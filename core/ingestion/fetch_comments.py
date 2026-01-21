import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


def fetch_comments(
    reddit,
    post_ids: List[str],
    comment_limit: int = 200,
    max_depth: int = 5,
) -> List[Dict]:
    """
    Fetch and flatten Reddit comments for a list of post IDs.

    Args:
        reddit: Authenticated PRAW Reddit client
        post_ids (List[str]): List of Reddit submission IDs
        comment_limit (int): Max number of comments per post
        max_depth (int): Max depth of comment tree to include

    Returns:
        List[Dict]: List of comment TextUnits
    """

    all_comments: List[Dict] = []

    for post_id in post_ids:
        try:
            logger.info(f"Fetching comments for post_id={post_id}")

            submission = reddit.submission(id=post_id)

            # Expand all 'MoreComments'
            submission.comments.replace_more(limit=0)

            collected = 0

            for comment in submission.comments.list():

                if collected >= comment_limit:
                    break

                if not hasattr(comment, "body"):
                    continue

                body = comment.body.strip()

                # Skip deleted, removed, empty comments
                if body in ("[deleted]", "[removed]", ""):
                    continue

                depth = getattr(comment, "depth", 0)
                if depth > max_depth:
                    continue

                comment_unit = {
                    "id": comment.id,
                    "post_id": post_id,
                    "parent_id": comment.parent_id,
                    "text": body,
                    "created_utc": int(comment.created_utc),
                    "score": comment.score,
                    "author": str(comment.author) if comment.author else None,
                    "source_type": "comment",
                    "depth": depth,
                }

                all_comments.append(comment_unit)
                collected += 1

            logger.info(
                f"Collected {collected} comments for post_id={post_id}"
            )

        except Exception as e:
            logger.warning(
                f"Failed to fetch comments for post_id={post_id}: {e}"
            )

    logger.info(f"Total comments collected: {len(all_comments)}")
    return all_comments
