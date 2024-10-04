from django.db.models import Q
from posts.models import Post, Tag
from posts.services import update_post_metadata

class SearchRepository:
    
    @staticmethod
    def search_by_post_or_tag(query_post_name):
        """
        Searches posts by title, body, or tag.

        Args:
            query_post_name: The name of the post or tag to search for.

        Returns:
            QuerySet: A queryset of filtered posts.
        """
        # Search for posts by title or body using Q objects
        posts_by_title_or_body = Post.objects.filter(
            Q(title__icontains=query_post_name) | Q(body__icontains=query_post_name)
        )
        
        # Capitalize the first letter of the tag query and filter by tags
        query_tag_name = query_post_name.capitalize()
        tag = Tag.objects.filter(name=query_tag_name).first()

        if tag:
            posts_by_tags = Post.objects.filter(tags=tag)
        else:
            posts_by_tags = Post.objects.none()

        # Combine the two queries using Q objects
        posts = Post.objects.filter(
            Q(id__in=posts_by_title_or_body.values_list('id', flat=True)) | 
            Q(id__in=posts_by_tags.values_list('id', flat=True))
        ).distinct()

        # Update post metadata
        return update_post_metadata(posts)
