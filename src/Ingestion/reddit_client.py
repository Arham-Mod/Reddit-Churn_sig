import os
import praw

def create_reddit_client(client_id, client_secret, user_agent):
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )
    return reddit
