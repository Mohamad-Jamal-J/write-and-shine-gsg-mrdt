from interactions.services import InteractionRepository
from posts.models import Post, Tag
from django.contrib.auth import get_user_model


def update_post_metadata(posts, user=None):
    """
    Update each post's likes count, comments count, and tags.
    
    Args:
        posts: QuerySet of posts.
        user: The current user.

    Returns:
        Updated posts with additional metadata.
    """
    for post in posts:
        post.likes_count = post.like_set.count()
        post.comments_count = post.comment_set.count()
        post.post_tags = post.tags.all()
        # Check if the user liked the post
        if user is not None:
            if user.is_authenticated:
                # Check if the user is authenticated and liked the post
                post.liked = InteractionRepository.user_liked_post(user, post.id)
            else:
                post.liked = False  # User is not logged in, set to False
    return posts


User = get_user_model()


class PostRepository:
    @staticmethod
    def create_post(title: str, body: str, author: User, tags: list[str]) -> Post:
        """
        Creates a new post and associates tags with it.

        Args:
            title (str): The post title.
            body (str): The post content.
            author (User): The user creating the post.
            tags (list[str]): A list of tag names.

        Returns:
            Post: The created post object.
        """
        post = Post.objects.create(title=title, body=body, author=author)
        
        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            post.tags.add(tag)
        
        return post

    @staticmethod
    def get_all_posts():
        """
        Retrieves all posts from the database.

        Returns:
            QuerySet: A queryset of all posts.
        """
        return Post.objects.all()

    @staticmethod
    def get_user_posts(user_id: int):
        """
        Retrieves all posts made by a specific user.

        Args:
            user_id (int): The ID of the user.

        Returns:
            QuerySet: A queryset of the user's posts.
        """
        return Post.objects.filter(author__id=user_id)
