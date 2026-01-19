import json
from groq import Groq
import os
import logging
from utils.logging.logger import setup_logging
from utils.config.load_config import load_yaml_config
from core.ingestion.reddit_client import create_reddit_client
from core.ingestion.fetch_posts import fetch_posts
from core.ingestion.fetch_comments import fetch_comments
from core.data_processing.save_raw import save_raw_posts
from core.data_processing.preprocessing.discussions import build_discussions
from core.llm_extraction.groq_client import get_groq_client
from core.data_processing.preprocessing.formatting import format_discussion_text
from core.data_processing.preprocessing.chunk_discussions import chunk_discussion
from core.llm_extraction.extract_signals import analyze_text_for_churn
from core.scoring.aggregrate_signals import aggregrate_churn_issues
from core.scoring.compute_risk_score import compute_churn_scores


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    # 1. Load Config
    config = load_yaml_config("utils/config/reddit.yaml")

    # 2. Create Reddit Client
    reddit_client = create_reddit_client()

    # 3. Ftech Posts (loggers inside func)
    posts = fetch_posts(
        reddit=reddit_client,
        subreddits=config["reddit"]["subreddits"],
        keywords=config["reddit"]["keywords"],
        post_limit=config["reddit"]["fetch"]["post_limit"],
        sort=config["reddit"]["fetch"]["sort"],
        time_filter=config["reddit"]["fetch"]["time_filter"]
    )


    # 4. Extract Correct post IDs
    post_ids = [p["id"] for p in posts]
    
    # 5. Fetch comments (loggers inside func)
    comments = fetch_comments(
        reddit=reddit_client,
        post_ids=post_ids,
        comment_limit=config["reddit"]["fetch"]["comment_limit"],
        max_depth=config["reddit"]["fetch"]["max_comment_depth"],
    )

    # 6. Save Raw Posts 
    save_raw_posts(posts)

    # 7. Save Raw Comments
    save_raw_posts(comments)

    # 7. Build Discussions
    discussions = build_discussions(posts, comments)

    # 8. Initialize LLM Client
    llm_client = get_groq_client()

    discussions_results = []

    # 9. Analyze discussions 

    for discussion in discussions:
        formatted_text = format_discussion_text(discussion)

        chunks = chunk_discussion(
            formatted_text
        )
        '''
        logging.info(f"Chunks created for post {discussion['post_id']}: {len(chunks)}")
    
        if not chunks:
            logging.warning(
                f"Skipping post {discussion['post_id']} — empty formatted text"
            )
            continue
        '''

        issues_for_post = []

        for chunk in chunks:
            result = analyze_text_for_churn(
            text=chunk,
            post_id=discussion["post_id"],
            llm_client=llm_client
            )

            if result:
                issues_for_post.extend(result["issues"])
                

        discussions_results.append({
            "post_id": discussion["post_id"],
            "issues": issues_for_post
        })

    # 10. Aggregrate issues
    aggregated = aggregrate_churn_issues(discussions_results)

    # 11. Compute Churn Scores
    ranked_issues = compute_churn_scores(aggregated)

    # 12. Output Results
    print("\n=== TOP CHURN RISKS ===\n")

    for issue in ranked_issues[:5]:
        print(f"Feature: {issue['affected_feature']}")
        print(f"Problem: {issue['problem_type']}")
        print(f"Churn Score: {issue['churn_score']}")
        print(f"Posts Affected: {issue['num_posts']}")
        print("Example Quote:")
        if issue["example_quotes"]:
            print(f"  - {issue['example_quotes'][0]}")
        print("-" * 40)

if __name__ == "__main__":
    main()