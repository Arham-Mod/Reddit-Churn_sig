def format_discussion_text(discussion: dict) -> str:
    """
    Convert a discussion into a single analysis ready text block.
    """

    parts = []

    title = discussion.get("title", "").strip()
    if title:
        parts.append(f"POST TITLE:\n{title}")

    body = discussion.get("post_body", "").strip()
    if body:
        parts.append(f"\nPOST BODY:\n{body}")

    comments = discussion.get("comments", [])
    if comments:
        parts.append("\nUSER COMMENTS:")
        for i, c in enumerate(comments[:30], 1):
            text = c.get("body", "").strip()
            if text:
                parts.append(f"{i}. {text}")

    formatted = "\n".join(parts).strip()

    return formatted
