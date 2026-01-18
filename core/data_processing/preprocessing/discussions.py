import logging
from typing import List, Dict
from collections import defaultdict

logger = logging.getLogger(__name__)


def build_discussions(
    posts: List[Dict],
    comments: List[Dict]
) -> List[Dict]:
    """
    Build discussion objects from post + comment records.
    """

    comments_by_post = defaultdict(list)

    for c in comments:
        comments_by_post[c["post_id"]].append(c)

    discussions: List[Dict] = []

    for post in posts:
        post_id = post["id"]

        title = post.get("text", "").split("\n", 1)[0].strip()
        post_body = post.get("text", "").split("\n", 1)[1].strip() if "\n" in post.get("text", "") else ""

        cleaned_comments = []

        for c in comments_by_post.get(post_id, []):
            body = c.get("text", "").strip()
            if not body:
                continue

            cleaned_comments.append({
                "comment_id": c["id"],
                "body": body,
                "score": c.get("score", 0),
                "author": c.get("author"),
                "created_utc": c.get("created_utc"),
                "depth": c.get("depth", 0)
            })

        discussion = {
            "post_id": post_id,
            "subreddit": post.get("subreddit"),
            "title": title,
            "post_body": post_body,
            "created_utc": post.get("created_utc"),
            "score": post.get("score", 0),
            "author": post.get("author"),
            "comments": cleaned_comments
        }

        logger.info(
            f"[DISCUSSION BUILT] post_id={post_id} | "
            f"title_len={len(title)} | "
            f"body_len={len(post_body)} | "
            f"comments={len(cleaned_comments)}"
        )

        discussions.append(discussion)

    logger.info(f"Built {len(discussions)} discussions")
    return discussions
