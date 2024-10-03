from posts.models import Post, Tag
from django.contrib.auth import get_user_model

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

