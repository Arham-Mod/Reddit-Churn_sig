def find_comments_for_posts(post, all_comments):
    """Returns comments belonging to a single post"""

    return [
        c for c in all_comments
        if c.get("post_id") == post.get("id")
    ]

