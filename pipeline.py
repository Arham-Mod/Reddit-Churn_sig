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


def run_pipeline(config, subreddit_override=None):
    setup_logging()
    logger = logging.getLogger(__name__)

    # override subreddit from Streamlit
    if subreddit_override:
        config["reddit"]["subreddits"] = [subreddit_override]

    reddit_client = create_reddit_client()

    posts = fetch_posts(
        reddit=reddit_client,
        subreddits=config["reddit"]["subreddits"],
        keywords=config["reddit"]["keywords"],
        post_limit=config["reddit"]["fetch"]["post_limit"],
        sort=config["reddit"]["fetch"]["sort"],
        time_filter=config["reddit"]["fetch"]["time_filter"]
    )

    post_ids = [p["id"] for p in posts]

    comments = fetch_comments(
        reddit=reddit_client,
        post_ids=post_ids,
        comment_limit=config["reddit"]["fetch"]["comment_limit"],
        max_depth=config["reddit"]["fetch"]["max_comment_depth"],
    )

    save_raw_posts(posts)
    save_raw_posts(comments)

    discussions = build_discussions(posts, comments)

    llm_client = get_groq_client()
    discussions_results = []

    for discussion in discussions:
        formatted_text = format_discussion_text(discussion)
        chunks = chunk_discussion(formatted_text)

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

    aggregated = aggregrate_churn_issues(discussions_results)
    ranked_issues = compute_churn_scores(aggregated)

    return ranked_issues
