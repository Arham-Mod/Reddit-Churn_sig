from core.data_processing.preprocessing.discussions import find_comments_for_posts
from core.data_processing.preprocessing.clean_text import clean_and_filter_comments

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
            "subreddit": post["subreddit"],
            "title": post["title"],
            "post_body": post["body"],
            "created_utc": post["created_utc"],

            "comments": cleaned_comments,

            "meta": {
                "num_comments": len(related_comments),
                "num_valid_comments": len(cleaned_comments)
            }
        }

        discussions.append(discussion)

    return discussions