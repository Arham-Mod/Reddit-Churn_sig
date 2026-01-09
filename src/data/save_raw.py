import json
import os
from datetime import datetime
from src.logging import logger

def save_raw_posts(posts, base_dir="data/raw"):
    """Saves raw Reddit posts to a JSON file with a timestamped filename."""

    os.makedirs(base_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(
        base_dir,
        f"raw_reddit_posts_{timestamp}.json"
    )

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

    logger.logging.info(
        "Saved %d posts to %s", len(posts), file_path
    )

    return file_path
