def chunk_text(text: str, chunk_size: int = 280, overlap: int = 35) -> list[str]:
    """
    Split cleaned text into overlapping word-based chunks for LLM processing.

    Args:
        text (str): Cleaned input text.
        chunk_size (int): Number of words per chunk.
        overlap (int): Number of overlapping words between consecutive chunks.

    Returns:
        list[str]: List of text chunks.
    """
    if not text:
        return []

    words = text.split()
    chunks = []

    start = 0
    step = chunk_size - overlap

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]
        chunks.append(" ".join(chunk_words))
        start += step

    return chunks
