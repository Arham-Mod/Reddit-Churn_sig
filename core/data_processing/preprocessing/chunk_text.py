import uuid
from typing import List, Dict

def chunk_text(
    text_units: List[Dict],
    max_tokens: int = 80,
    overlap: int =20
) -> List[Dict]:
    """
    Split cleaned text in each TextUnit into overlapping word-based chunks for LLM processing.
    """

    chunked_units: List[Dict] = []

    for unit in text_units:

        # Safety check
        if not isinstance(unit, dict):
            raise TypeError(
                f"chunk_text expected Dict but got {type(unit)}"
            )

        text = unit.get("text", "").strip()
        if not text:
            continue

        words = text.split()
        start = 0

        while start < len(words):
            end = start + max_tokens
            chunk_words = words[start:end]

            chunked_units.append({
                "chunk_id": str(uuid.uuid4()),
                "source_type": unit["source_type"],
                "text": " ".join(chunk_words),
                "created_utc": unit["created_utc"],
                "subreddit": unit["subreddit"],

                # Explicit linkage
                "post_id": unit["post_id"],
                "comment_id": unit.get("id") if unit["source_type"] == "comment" else None,
                "parent_comment_id": unit.get("parent_comment_id"),

                "author": unit.get("author"),

                # All non-core fields live here
                "metadata": {
                    "score": unit.get("score"),
                    "depth": unit.get("depth", 0)
                }
            })

            start += max_tokens - overlap
        return chunked_units

