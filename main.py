import logging
from utils.logging.logger import setup_logging
from utils.config.load_config import load_yaml_config
from core.ingestion.reddit_client import create_reddit_client
from core.ingestion.fetch_posts import fetch_posts
from core.data_processing.save_raw import save_raw_posts
from core.data_processing.preprocessing.preprocess_pipeline import preprocess_raw_data
from core.ingestion.fetch_comments import fetch_comments


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
    #TRY THIS CODE IN MAIN FILE TO CHECK THESE LOGS ARE WORKING OR NOT AND PRESENT IN THE FETCH_POSTS FILE

    '''
    print(f"Fetched {len(posts)} posts")
    logger.info("Fetched %d posts", len(posts))

    if posts:
        print("Sample post title:", posts[0]["title"])
    '''

    # 4. Fetch Comments
    post_ids = [p["post_id"] for p in posts]

    comments = fetch_comments(
    reddit=reddit_client,
    post_ids=post_ids,
    comment_limit=config["reddit"]["fetch"]["comment_limit"],
    max_depth=config["reddit"]["fetch"]["max_comment_depth"],
    )

    text_units = posts + comments


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
