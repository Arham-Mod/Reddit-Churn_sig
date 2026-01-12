import uuid
from typing import List, Dict

def chunk_text(
    text_units: List[Dict],
    max_tokens: int = 80,
    overlap: int = 20
) -> List[Dict]:
    """
    Chunk text per TextUnit while preserving metadata.
    """

    chunked_units: List[Dict] = []

    for unit in text_units:

        # DEFENSIVE CHECK (this prevents silent bugs)
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
                "text": " ".join(chunk_words),
                "unit_id": unit["id"],
                "post_id": unit["post_id"],
                "source_type": unit["source_type"],
                "author": unit.get("author"),
                "created_utc": unit["created_utc"],
                "depth": unit.get("depth", 0),
            })

            start += max_tokens - overlap

    return chunked_units
