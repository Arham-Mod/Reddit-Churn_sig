import logging
from utils.logging.logger import setup_logging
from utils.config.load_config import load_yaml_config
from core.ingestion.reddit_client import create_reddit_client
from core.ingestion.fetch_posts import fetch_posts
from core.ingestion.fetch_comments import fetch_comments
from core.data_processing.save_raw import save_raw_comments, save_raw_posts
from core.data_processing.preprocessing.preprocess_pipeline import load_json, preprocess_raw_data
import json
from groq import Groq
import os
from core.llm_extraction.extract_signals import extract_churn_signals


def load_taxonomy(taxonomy_path: str) -> dict:
        with open(taxonomy_path, "r", encoding="utf-8") as f:
            return json.load(f)
        

def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    # 1. Load config
    config = load_yaml_config("utils/config/reddit.yaml")

    # 2. Create Reddit client
    reddit_client = create_reddit_client()

    # 3. Fetch posts
    posts = fetch_posts(
        reddit=reddit_client,
        subreddits=config["reddit"]["subreddits"],
        keywords=config["reddit"]["keywords"],
        post_limit=config["reddit"]["fetch"]["post_limit"],
        sort=config["reddit"]["fetch"]["sort"],
        time_filter=config["reddit"]["fetch"]["time_filter"]
    )

    logger.info("Fetched %d posts", len(posts))

    # 4. Save raw posts
    try:
        posts_raw_file_path = save_raw_posts(posts=posts)
        logger.info("Raw posts saved to: %s", posts_raw_file_path)
    except Exception:
        logger.exception("Failed to save raw posts")
        raise

    # 5. Extract CORRECT post IDs
    post_ids = [p["id"] for p in posts]

    # 6. Fetch comments (ONCE)
    comments = fetch_comments(
        reddit=reddit_client,
        post_ids=post_ids,
        comment_limit=config["reddit"]["fetch"]["comment_limit"],
        max_depth=config["reddit"]["fetch"]["max_comment_depth"],
    )

    logger.info("Fetched %d comments", len(comments))

    # 7. Save raw comments
    try:
        comments_raw_file_path = save_raw_comments(comments=comments)
        logger.info("Raw comments saved to: %s", comments_raw_file_path)
    except Exception:
        logger.exception("Failed to save raw comments")
        raise

    logger.info(
        "Passing comments_path to preprocessing: %s",
        comments_raw_file_path
    )

    # 8. Preprocess (LAST STEP)
    try:
        preprocess_raw_data(
            posts_path=posts_raw_file_path,
            comments_path=comments_raw_file_path,
            product_name=config["product"]["name"]
        )
        logger.info("Preprocessing completed successfully")
    except Exception:
        logger.exception("Preprocessing failed")
        raise

    #9. Load taxonomy
    
    
    taxonomy = load_taxonomy("core/llm_extraction/churn_signal_taxonomy.json")

    #10. Groq llm client initialization
    client = Groq(
        api_key="GET LOGIC TO INTAKE API FROM ENV DIRECTLY",
    )
    #need changes

    preprocessed_texts=load_json("data/processed/clean_chunks.json")

    results = []

    for text in preprocessed_texts:
        signals = extract_churn_signals(
            text=text,
            taxonomy=taxonomy,
            llm_client=client
        )

        results.append({
            "text": text,
            "signals": signals
        })

    for r in results:
        print("=" * 80)
        print("TEXT:", r["text"])
        print("SIGNALS:", r["signals"])


if __name__ == "__main__":
    main()
