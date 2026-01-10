from src.logging import logger
from src.config.load_config import load_yaml_config
from src.ingestion.reddit_client import create_reddit_client
from src.ingestion.fetch_posts import fetch_posts
from src.data.save_raw import save_raw_posts
from src.preprocessing.preprocess_pipeline import preprocess_raw_data


def main():
    # 1. Load config
    try:
        config = load_yaml_config("src/config/reddit.yaml")
        logger.logging.info("Config loaded successfully")
        logger.logging.info("Config keys: %s", list(config.keys()))
    except Exception:
        logger.logging.exception("Failed to load configuration")
        raise

    # 2. Create Reddit client
    try:
        reddit_client = create_reddit_client()
        logger.logging.info("Reddit client created successfully")
    except Exception:
        logger.logging.exception("Failed to create Reddit client")
        raise

    # 3. Fetch posts
    posts = fetch_posts(
        reddit=reddit_client,
        subreddits=config["reddit"]["subreddits"],
        post_limit=config["reddit"]["fetch"]["post_limit"],
        keywords=config["reddit"]["keywords"]
    )

    print(f"Fetched {len(posts)} posts")
    logger.logging.info("Fetched %d posts", len(posts))

    if posts:
        print("Sample post title:", posts[0]["title"])

    # 4. Save raw posts
    try:
        raw_file_path = save_raw_posts(posts=posts)
        logger.logging.info("Raw posts saved to: %s", raw_file_path)
    except Exception:
        logger.logging.exception("Failed to save raw posts")
        raise

    # 5. Preprocess raw posts
    try:
        preprocess_raw_data(
            posts_path=raw_file_path,
            product_name=config["product"]["name"]
        )
        logger.logging.info("Preprocessing completed successfully")
    except Exception:
        logger.logging.exception("Preprocessing failed")
        raise


if __name__ == "__main__":
    logger.logging.info("Starting the Reddit Churn Prediction Application")
    main()
