import logging
from utils.logging import logger
from utils.logging.logger import setup_logging
from utils.config.load_config import load_yaml_config
from src.ingestion.reddit_client import create_reddit_client
from src.ingestion.fetch_posts import fetch_posts
from src.data_processing.save_raw import save_raw_posts
from src.data_processing.preprocessing.preprocess_pipeline import preprocess_raw_data


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    # 1. Load config
    try:
        config = load_yaml_config("utils/config/reddit.yaml")
        logger.info("Config loaded successfully")
        logger.info("Config keys: %s", list(config.keys()))
    except Exception:
        logger.exception("Failed to load configuration")
        raise

    # 2. Create Reddit client
    try:
        reddit_client = create_reddit_client()
        logger.info("Reddit client created successfully")
    except Exception:
        logger.exception("Failed to create Reddit client")
        raise

    # 3. Fetch posts
    posts = fetch_posts(
    reddit=reddit_client,
    subreddits=config["reddit"]["subreddits"],
    keywords=config["reddit"]["keywords"],
    post_limit=config["reddit"]["fetch"]["post_limit"],
    sort=config["reddit"]["fetch"]["sort"],
    time_filter=config["reddit"]["fetch"]["time_filter"]
)


    print(f"Fetched {len(posts)} posts")
    logger.info("Fetched %d posts", len(posts))

    if posts:
        print("Sample post title:", posts[0]["title"])

    # 4. Save raw posts
    try:
        raw_file_path = save_raw_posts(posts=posts)
        logger.info("Raw posts saved to: %s", raw_file_path)
    except Exception:
        logger.exception("Failed to save raw posts")
        raise

    # 5. Preprocess raw posts
    try:
        preprocess_raw_data(
            posts_path=raw_file_path,
            product_name=config["product"]["name"]
        )
        logger.info("Preprocessing completed successfully")
    except Exception:
        logger.exception("Preprocessing failed")
        raise


if __name__ == "__main__":
    main()
