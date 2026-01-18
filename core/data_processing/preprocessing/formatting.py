from typing import List, Dict

def format_discussion_text(
        discussions: Dict,
        max_comments: int=50
) -> str:
    """
    Convert a Discussion object into a single, coherent text block
    suitable for LLM analysis.

    Parameters:
    - discussion: A Discussion dict (post + comments)
    - max_comments: Max number of comments to include (safety + signal control)

    Returns:
    - A formatted string representation of the discussion
    """

    title = discussions.get("title", "").strip()
    post_body = discussions.get("post_body", "").strip()
    comments: List[Dict] = discussions.get("comments",[])

    comments = comments[:max_comments]

    # -------- Post title --------
    if title:
        formatted_parts.append("POST TITLE:")
        formatted_parts.append(title)
        formatted_parts.append("")
    
    # -------- Post body --------
    if post_body:
        formatted_parts.append("POST BODY:")
        formatted_parts.append(post_body)
        formatted_parts.append("")

    # -------- Comments --------
    if comments:
        formatted_parts.append("USER COMMENTS:")
        for idx, comments in enumerate(comments, start=1):
            body = comments.get("bosy", "").strip()
            if body:
                formatted_parts.append(f"{idx}.{body}")
    
    return "\n".join(formatted_parts)