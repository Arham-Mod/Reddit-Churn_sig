from core.data_processing.preprocessing.clean_text import clean_and_filter_comments
from core.data_processing.preprocessing.grouping import find_comments_for_posts
from typing import List, Dict

def build_discussions(posts,comments) -> List[Dict]:
    '''
    Input: 
        posts: raw list of posts
        comments: raw list of comments
    
    Output:
        List[Discussions]
    '''

    discussions = []

    for post in posts:
        related_comments = find_comments_for_posts(post,comments)

        cleaned_comments = clean_and_filter_comments(related_comments)

        discussion = {
            "post_id": post["id"],
            "subreddit": (
                post.get("subreddit")
                or post.get("subreddit_name_prefixed")
                or post.get("subreddit_name")
                or "unknown"
            ),
            "title": post.get("title", "").strip(),
            "post_body": post.get("body") or post.get("selftext", ""),
            "created_utc": post.get("created_utc"),

            "comments": cleaned_comments,

            "meta": {
                "num_comments": len(related_comments),
                "num_valid_comments": len(cleaned_comments)
            }
        }

        discussions.append(discussion)

    return discussions