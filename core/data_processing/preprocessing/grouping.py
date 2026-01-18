def find_comments_for_posts(post,all_comments):
    '''returns comments belonging to single post'''

    return{
        c for c in all_comments
        if c["post_id"] == post["id"]
    }