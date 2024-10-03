def update_post_metadata(posts):
    """
    Update each post's likes count, comments count, and tags.
    """
    for post in posts:
        post.likes_count = post.like_set.count()
        post.comments_count = post.comment_set.count()
        post.post_tags = post.tags.all()
    return posts
