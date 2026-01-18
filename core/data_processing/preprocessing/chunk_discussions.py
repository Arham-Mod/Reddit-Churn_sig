from typing import List

def chunk_dicussion(discussions, max_chars) -> List[str]:
    text = format_discussion_text(discussions)

    if len(text) <= max_chars:
        return [text]
    
    return split_into_large_chunks(text)
    