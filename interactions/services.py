from posts.models import Post
from interactions.models import Comment, Like
from django.shortcuts import get_object_or_404

class InteractionRepository:
    @staticmethod
    def toggle_like(user, post_id):
        """
        Toggles the like for a post. If the user has liked it, the like will be removed, otherwise, it will be added.

        Args:
            user: The user liking/unliking the post.
            post_id: The ID of the post to like/unlike.

        Returns:
            dict: A dictionary containing the success status and message.
        """
        post = get_object_or_404(Post, pk=post_id)
        like_instance = Like.objects.filter(user=user, post=post).first()

        if like_instance:
            like_instance.delete()
            return {'success': True, 'message': 'Like removed.'}

        Like.objects.create(user=user, post=post)
        return {'success': True, 'message': 'Like added.'}

    @staticmethod
    def add_comment(user, post_id, comment_body):
        """
        Adds a comment to a post.

        Args:
            user: The user adding the comment.
            post_id: The ID of the post to comment on.
            comment_body: The body of the comment.

        Returns:
            dict: A dictionary containing the success status and message.
        """
        if not comment_body:
            return {'success': False, 'message': 'Comment cannot be empty.'}

        post = get_object_or_404(Post, pk=post_id)
        Comment.objects.create(post=post, author=user, body=comment_body)
        return {'success': True, 'message': 'Comment added.'}

    @staticmethod
    def get_comment(comment_id):
        """
        Retrieves a comment by its ID.

        Args:
            comment_id: The ID of the comment.

        Returns:
            dict: A dictionary containing the success status, comment object, and message.
        """
        try:
            comment = Comment.objects.get(pk=comment_id)
            return {'success': True, 'comment': comment}
        except Comment.DoesNotExist:
            return {'success': False, 'message': 'Comment not found.'}

    @staticmethod
    def update_comment_body(comment, new_body):
        """
        Updates the body of a comment.

        Args:
            comment: The comment object to update.
            new_body: The new content of the comment.

        Returns:
            None
        """
        comment.body = new_body
        comment.save()

    @staticmethod
    def delete_comment(comment):
        """
        Deletes a comment.

        Args:
            comment: The comment object to delete.

        Returns:
            None
        """
        comment.delete()


    @staticmethod
    def user_liked_post(user, post_id):
        try:
            post = Post.objects.get(id=post_id)
            return Like.objects.filter(user=user, post=post).exists()
        except Post.DoesNotExist:
            return False
