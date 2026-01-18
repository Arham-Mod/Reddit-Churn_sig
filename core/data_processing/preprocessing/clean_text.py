import re


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def clean_and_filter_comments(comments):
    cleaned = []

    for c in comments:
        body = c.get("body", "")

        if body in ("[deleted]", "[removed]"):
            continue

        body = normalize_text(body)

        if len(body.split()) < 5:
            continue

        cleaned.append({
            "comment_id": c["id"],
            "body": body,
            "score": c.get("score", 0),
            "created_utc": c.get("created_utc")
        })

    return cleaned
