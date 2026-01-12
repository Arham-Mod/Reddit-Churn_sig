import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def fetch_posts(
    reddit,
    subreddits: List[str],
    keywords: List[str],
    post_limit: int,
    sort: str = "new",
    time_filter: str = "month"
) -> List[Dict]:

    all_posts = []
    seen_post_ids = set()   # prevent duplicates across keywords/subreddits

    for subreddit_name in subreddits:
        logger.info(f"Fetching posts from r/{subreddit_name}")

        subreddit = reddit.subreddit(subreddit_name)

        # Select sorting strategy
        if sort == "hot":
            submissions = subreddit.hot(limit=post_limit)
        elif sort == "top":
            submissions = subreddit.top(time_filter=time_filter, limit=post_limit)
        else:
            submissions = subreddit.new(limit=post_limit)

        for submission in submissions:
            # Deduplicate posts
            if submission.id in seen_post_ids:
                continue

            combined_text = f"{submission.title}\n{submission.selftext}".lower()

            # Keyword filtering
            if not any(keyword.lower() in combined_text for keyword in keywords):
                continue

            post_unit = {
                "id": submission.id,
                "post_id": submission.id,
                "parent_id": None,
                "text": submission.title + "\n" + submission.selftext,
                "created_utc": int(submission.created_utc),
                "score": submission.score,
                "author": str(submission.author) if submission.author else None,
                "source_type": "post",
                "depth": 0
            }

            all_posts.append(post_unit)
            seen_post_ids.add(submission.id)

        logger.info(
            f"Collected {len(all_posts)} posts so far from r/{subreddit_name}"
        )

    logger.info(f"Total posts collected: {len(all_posts)}")
    return all_posts
