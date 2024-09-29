from django.shortcuts import render
from rest_framework.decorators import api_view
from posts.models import Post, Tag
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, 'search/index.html')


def update_post_metadata(posts):
    """
    Update each post's likes count, comments count, and tags.
    """
    for post in posts:
        post.likes_count = post.like_set.count()
        post.comments_count = post.comment_set.count()
        post.post_tags = post.tags.all()
    return posts


@api_view(['GET'])
def search_post(request):
    query_post_name = request.GET.get('post_name', '').strip()
    
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
    posts = update_post_metadata(posts)

    return render(request, 'posts.html', {'posts': posts})


@api_view(['GET'])
def get_posts(request):
    posts = Post.objects.all()

    # Update post metadata
    posts = update_post_metadata(posts)

    return render(request, 'posts.html', {'posts': posts})