import os
import logging
import praw

def create_reddit_client():
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")

    if not all([client_id, client_secret, user_agent]):
        logging.error(
            f"Missing Reddit credentials: "
            f"client_id={bool(client_id)}, "
            f"client_secret={bool(client_secret)}, "
            f"user_agent={bool(user_agent)}"
        )
        raise ValueError("Reddit credentials not found in environment variables")

    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        logging.info("Reddit client created successfully")
        return reddit
    except Exception as e:
        logging.exception("Failed to create Reddit client")
        raise
