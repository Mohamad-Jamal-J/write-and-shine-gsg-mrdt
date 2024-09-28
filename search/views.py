from django.shortcuts import render
from rest_framework.decorators import api_view
from posts.models import Post, Tag
from posts.serializers import PostSerializer

# Create your views here.
def index(request):
    return render(request, 'search/index.html')



@api_view(['GET'])
def search_post(request):
    query_post_name = request.GET.get('post_name', '')

    posts = Post.objects.filter(title__icontains=query_post_name) | Post.objects.filter(body__icontains=query_post_name)

    serializer = PostSerializer(posts, many=True)  
    return render(request, 'posts.html', {'posts': serializer.data})


@api_view(['GET'])
def get_posts(request):
    tag_name = request.GET.get('tag', '').strip().capitalize()  # Get tag from query parameter and capitalize

    if tag_name:
        tag = Tag.objects.filter(name=tag_name).first()

        if tag:
            posts = Post.objects.filter(tags=tag).distinct()  # Use 'tags' instead of 'post_tag__tag'
        else:
            posts = Post.objects.none()
    else:
        posts = Post.objects.all()

    for post in posts:
        post.likes_count = post.like_set.count()
        post.comments_count = post.comment_set.count()
        post.post_tags = post.tags.all() 

    return render(request, 'posts.html', {'posts': posts})