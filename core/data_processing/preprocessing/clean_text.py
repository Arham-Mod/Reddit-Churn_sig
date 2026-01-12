import uuid
from typing import List, Dict
import re

def clean_text(text_units: List[Dict]) -> List[Dict]:
    """
    Cleans the 'text' field of each TextUnit while preserving structure.
    """

    cleaned_units: List[Dict] = []

    for unit in text_units:
        # Safety check
        if not isinstance(unit, dict):
            raise TypeError(
                f"clean_text expected Dict but got {type(unit)}"
            )

        raw_text = unit.get("text", "")

        # Basic cleaning (extend later)
        text = raw_text.lower()
        text = re.sub(r"http\S+", "", text)   # remove URLs
        text = re.sub(r"\s+", " ", text)      # normalize spaces
        text = text.strip()

        # IMPORTANT: preserve structure
        new_unit = unit.copy()
        new_unit["text"] = text

        cleaned_units.append(new_unit)

    return cleaned_units



def is_valid_text(text: str, min_words: int = 15) -> bool:
    if not text:
        return False

    if text.strip() in {"[deleted]", "[removed]"}:
        return False

    return len(text.split()) >= min_words
