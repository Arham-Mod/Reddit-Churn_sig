import re
"regex library for text cleaning"

import re

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove URLs only (LLMs don't need them)
    text = re.sub(r"http\S+|www\S+", "", text)

    # Strip leading/trailing spaces
    text = text.strip()

    return text.lower()

def is_valid_text(text: str, min_words: int = 15) -> bool:
    if not text:
        return False

    if text.strip() in {"[deleted]", "[removed]"}:
        return False

    return len(text.split()) >= min_words
