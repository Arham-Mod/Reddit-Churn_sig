import json 
import logging
import uuid
from datetime import datetime, timezone
from pathlib import Path

from src.data_processing.preprocessing.chunk_text import chunk_text
from src.data_processing.preprocessing.clean_text import clean_text, is_valid_text


def get_latest_raw_posts_file(raw_dir="data/raw") -> str:
    files = list(Path(raw_dir).glob("raw_reddit_posts_*.json"))
    if not files:
        raise FileNotFoundError("No raw Reddit post files found")
    return str(max(files, key=lambda f: f.stat().st_mtime))


def load_json(path: str) -> list:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return json.load(f)


def save_json(data: list, path: str) -> None:
    """Saves processed data to a JSON file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def preprocess_raw_data(
    posts_path: str,
    product_name: str,
    output_path: str = "data/processed/clean_chunks.json"
    ) -> list:

    posts = load_json(posts_path)
    processed_chunks = []

    run_timestamp = datetime.now(timezone.utc).isoformat()

    skipped_posts = 0
    skipped_chunks = 0

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


            cleaned_text = clean_text(raw_text)

            # If text is completely empty, skip early
            if not cleaned_text:
                skipped_posts += 1
                continue
            logging.info(f"Total posts to process: {len(posts)}")
    except Exception as e:
        logging.error("Error processing posts")
        
    try:
        # Chunk FIRST
        chunks = chunk_text(cleaned_text)

        # Validate EACH chunk
        for chunk in chunks:
            if not is_valid_text(chunk):
                skipped_chunks += 1
                continue

            processed_chunks.append({
                "chunk_id": str(uuid.uuid4()),
                "text": chunk,
                "source_type": "post",
                "post_id": post.get("id"),
                "subreddit": post.get("subreddit"),
                "created_utc": post.get("created_utc"),
                "product": product_name,
                "run_timestamp": run_timestamp
            })
            logging.info(f"processed chunks count: {len(processed_chunks)}")
            logging.info("Preprocessing completed successfully")

    except Exception as e:
        logging.error("Error processing chunks")
        logging.info("preprocessing failed")
        raise e
    
    save_json(processed_chunks, output_path)
    logging.info(f"Processed chunks saved to: {output_path}")
    return processed_chunks



