import os
import praw
import logging

def create_reddit_client():
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")

    
    

    logging.info("Creating Reddit client")

    try:
        reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
        )
        logging.info("Reddit client created successfully")
    except Exception as e:
        if not client_id or not client_secret or not user_agent:
            logging.error("Missing Reddit API credentials in environment variables")
        raise ValueError("Failed to create Reddit client")

    return reddit