import json 
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path

# check below both lines for error as these files do not exist
'''
from core.data_processing.preprocessing.chunk_text import chunk_text
from core.data_processing.preprocessing.clean_text import clean_text, is_valid_text
'''

# Functions to get latest raw data files
def get_latest_raw_posts_file(raw_dir="data/raw") -> str:
    files = list(Path(raw_dir).glob("raw_reddit_posts_*.json"))
    if not files:
        raise FileNotFoundError("No raw Reddit post files found")
    return str(max(files, key=lambda f: f.stat().st_mtime))


# Functions to get latest raw data files
def get_latest_raw_comments_file(raw_dir="data/raw") -> str:
    files = list(Path(raw_dir).glob("raw_reddit_comments_*.json"))
    if not files:
        raise FileNotFoundError("No raw Reddit comment files found")
    return str(max(files, key=lambda f: f.stat().st_mtime))


# Load JSON data
def load_json(path: str) -> list:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return json.load(f)


# Save JSON data
def save_json(data: list, path: str) -> None:
    """Saves processed data to a JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# Preprocess raw data
def preprocess_raw_data(
    posts_path: str,
    comments_path: str | None,
    product_name: str,
    output_path: str = "data/processed/clean_chunks.json"
) -> list:


    posts = load_json(posts_path)
    processed_chunks = []

    run_timestamp = datetime.now(timezone.utc).isoformat()

    skipped_posts = 0
    skipped_chunks = 0

    text_units = []   

    try:
        for post in posts:
            title = post.get("title", "")
            text = post.get("text", "")

            # Ensure both are strings
            if not isinstance(title, str):
                title = ""
            if not isinstance(text, str):
                text = ""

            raw_text = f"{title} {text}".strip()

            # Skip empty text early
            if not raw_text:
                skipped_posts += 1
                continue

            text_units.append({
                "id": post.get("id"),
                "post_id": post.get("id"),
                "parent_comment_id": None,
                "text": raw_text,
                "source_type": "post",
                "subreddit": post.get("subreddit"),
                "created_utc": post.get("created_utc"),
                "author": post.get("author"),
                "score": post.get("score"),
                "depth": 0
            })

        logging.info(f"Total posts to process: {len(text_units)}")

    except Exception as e:
        logging.error("Error processing posts")
        raise e


    # comment ingestion
    try:
        comments_path = get_latest_raw_comments_file()
        comments = load_json(comments_path)

        for comment in comments:
            body = comment.get("text", "")

            if not isinstance(body, str):
                continue

            body = body.strip()
            if not body:
                continue

            text_units.append({
                "id": comment.get("id"),
                "post_id": comment.get("post_id"),
                "parent_comment_id": comment.get("parent_id"),
                "text": body,
                "source_type": "comment",
                "subreddit": comment.get("subreddit"),
                "created_utc": comment.get("created_utc"),
                "author": comment.get("author"),
                "score": comment.get("score"),
                "depth": comment.get("depth", 1)
            })

        logging.info(f"Total text units after comments: {len(text_units)}")

    except FileNotFoundError:
        logging.info("No raw comment file found; preprocessing posts only")

    except Exception as e:
        logging.error("Error processing comments")
        raise e
    
    logging.info(f"Chunks after validation: {len(processed_chunks)}")
    return processed_chunks
