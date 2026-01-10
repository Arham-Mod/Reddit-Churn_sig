import re
"regex library for text cleaning"

def clean_text(text: str) -> str:
    """Cleans the input text by removing URLs, special characters, and extra whitespace.
    """
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    """
    removes urls and replaces with empty string
    uses regex pattern http\S+ to match urls starting with http or https
    """

    text = re.sub(r"\S+", " ", text)
    """
    removes special characters and replaces with empty string
    uses regex pattern \S+ to match any non-whitespace character
    """

    return text.strip()
    """
    removes leading and trailing whitespace
    """

def is_valid_text(text: str, min_words: int = 5) -> bool:
    """Checks if the cleaned text meets the minimum word count requirement.
    """
    if not text:
        return False
    
    if text in {"[deleted]", "[removed]"}:
        return False
    
    if len(text.split()) < min_words:
        return False    
    
    return True
