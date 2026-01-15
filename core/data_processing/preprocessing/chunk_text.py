import uuid
import logging
from typing import List, Dict

def chunk_text(
    text_units: List[Dict],
    max_tokens: int = 80,
    overlap: int = 20
) -> List[Dict]:
    """
    Create chunks from individual posts and comments.
    Each post/comment is treated independently.
    """

    chunked_units: List[Dict] = []

    for unit in text_units:

        if not isinstance(unit, dict):
            raise TypeError(
                f"chunk_text expected Dict but got {type(unit)}"
            )

        text = unit.get("text", "").strip()
        if not text:
            continue

        words = text.split()

        # -------- CASE 1: short text → single chunk --------
        if len(words) <= max_tokens:
            chunked_units.append(_build_chunk(unit, text))
            continue

        # -------- CASE 2: long text → sliding window --------
        start = 0
        while start < len(words):
            end = start + max_tokens
            chunk_text = " ".join(words[start:end])

            chunked_units.append(_build_chunk(unit, chunk_text))

            start += max_tokens - overlap

    logging.info(
        f"Chunking completed | input_units={len(text_units)} | chunks_created={len(chunked_units)}"
    )

    return chunked_units


def build_chunk(unit: Dict, text: str) -> Dict:
    """
    Helper to build a chunk dict with correct metadata.
    """
    return {
        "chunk_id": str(uuid.uuid4()),
        "source_type": unit.get("source_type"),  # post / comment
        "text": text,

        # linkage
        "post_id": unit.get("post_id"),
        "comment_id": unit.get("id") if unit.get("source_type") == "comment" else None,
        "parent_comment_id": unit.get("parent_comment_id"),

        # metadata
        "author": unit.get("author"),
        "subreddit": unit.get("subreddit"),
        "created_utc": unit.get("created_utc"),
        "metadata": {
            "score": unit.get("score"),
            "depth": unit.get("depth", 0)
        }
    }
