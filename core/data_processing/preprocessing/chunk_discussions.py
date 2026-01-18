from typing import List


def chunk_discussion(text: str, max_chars: int = 4000) -> List[str]:
    if not text or not text.strip():
        return []

    if len(text) <= max_chars:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        chunks.append(text[start:start + max_chars])
        start += max_chars

    return chunks
