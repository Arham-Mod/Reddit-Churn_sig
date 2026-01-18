from typing import List

from typing import List


def chunk_discussion(text: str, max_chars: int = 4000) -> List[str]:
    """
    Defensive chunking: returns non-empty chunks only.
    """

    if not text or not text.strip():
        return []

    if len(text) <= max_chars:
        return [text]

    return split_into_large_chunks(text, max_chars)



def split_into_large_chunks(
    text: str,
    max_chars: int = 4000
) -> List[str]:
    """
    Split a large formatted discussion text into a small number of
    large, coherent chunks based on paragraph boundaries.

    Parameters:
    - text: formatted discussion text (string)
    - max_chars: maximum characters per chunk

    Returns:
    - List of text chunks (strings)
    """

    # Split by paragraph boundaries
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    chunks: List[str] = []
    current_chunk: List[str] = []
    current_length = 0

    for para in paragraphs:
        para_len = len(para)

        # Case 1: paragraph itself is too large → hard split
        if para_len > max_chars:
            if current_chunk:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = []
                current_length = 0

            # Hard split oversized paragraph
            for i in range(0, para_len, max_chars):
                chunks.append(para[i:i + max_chars])

            continue

        # Case 2: normal accumulation
        if current_length + para_len <= max_chars:
            current_chunk.append(para)
            current_length += para_len
        else:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = [para]
            current_length = para_len

    # Append last chunk
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks
