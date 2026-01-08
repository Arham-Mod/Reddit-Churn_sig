def fetch_posts(reddit, subreddits, keywords, post_limit):
    all_posts = []

    for subreddit in subreddits:
        subreddit_obj = reddit.subreddit(subreddit)

    for keyword in keywords:
        posts = subreddit_obj.search(query = keyword, limit = post_limit)

        for post in posts:
            post_data = {
                "id": post.id,
                "title": post.title,
                "text": post.selftext,
                "created_utc": post.created_utc,
                "score": post.score,
                "subreddit": subreddit,
                "keyword": keyword
            }
            all_posts.append(post_data)


    return all_posts
    
