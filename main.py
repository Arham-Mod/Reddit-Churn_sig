from src.logging import logger
from src.config.load_config import load_yaml_config
from src.ingestion.reddit_client import create_reddit_client
from src.ingestion.fetch_posts import fetch_posts
from src.data.save_raw import save_raw_posts

def main():
    try:
        config = load_yaml_config("src/config/reddit.yaml")
        logger.logging.info("Config loaded successfully")
        logger.logging.info("Config keys: %s", list(config.keys()))
    except Exception as e:
        logger.logging.exception("Failed to load configuration")
        raise

    try:
        reddit_client = create_reddit_client()
        logger.logging.info("Reddit client created successfully")

    except Exception as e:
        logger.logging.exception("Failed to create Reddit client")
        raise

    posts = fetch_posts(
        reddit=reddit_client,
        subreddits=config["reddit"]["subreddits"],
        post_limit=config["reddit"]["fetch"]["post_limit"],
        keywords=config["reddit"]["keywords"]
    )

    # 4. Simple verification output
    print(f"Fetched {len(posts)} posts")
    logger.logging.info("Fetched %d posts", len(posts))

    # Optional: inspect first post
    if posts:
        print("Sample post title:", posts[0]["title"])

    # Save raw posts
    try:
        file_path = save_raw_posts(posts=posts)
        logger.logging.info(f"Raw posts saved to: {file_path}")

    except Exception as e:
        logger.logging.exception("Failed to save raw posts")
        raise

if __name__ == "__main__":
    logger.logging.info("Starting the Reddit Churn Prediction Application")
    main()