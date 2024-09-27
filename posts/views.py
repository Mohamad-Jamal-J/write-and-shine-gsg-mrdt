from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from posts.models import Comment, Like, Post, Tag
from posts.serializers import PostSerializer
from django.utils import timezone


def index(request):
    return render(request, 'posts/index.html')  


def create_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':  # The user clicked the button to create a post
            title = request.POST.get('title')
            body = request.POST.get('body')
            tags = request.POST.getlist('tags')

            if title and body:
                post = Post.objects.create(
                    title=title,
                    body=body,
                    author=request.user  # Set the logged-in user as the author
                )

                for tag_name in tags:
                    tag_name = tag_name.strip().capitalize()  # Capitalize and trim whitespace
                    tag, created = Tag.objects.get_or_create(name=tag_name)  # Get or create the tag
                    post.tags.add(tag)  # Associate the tag with the post using the ManyToManyField

                return HttpResponse("Post created successfully!")
                # If you want to redirect to the home page:
                # return redirect('home')

            return HttpResponse("The post data is not valid", status=400)

        elif request.method == 'GET':
            # The form to create the post
            return render(request, 'create_post.html')

    else:
        return HttpResponse("You should be logged in to create a post", status=403)


from rest_framework.decorators import api_view
from django.shortcuts import render
from .models import Post, Tag

@api_view(['GET'])
def get_all_posts(request):
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
        print(post.post_tags)

    return render(request, 'posts.html', {'posts': posts})



@api_view(['DELETE', 'POST', 'GET'])
def delete_edit_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_id)

        # Check if the authenticated user is the author of the post
        if post.author != request.user:
            return Response({"message": "You do not have permission to edit or delete this post."}, status=403)

        if request.method == 'GET':
            # Handle the edit action
            if 'edit' in request.GET:
                return render(request, 'post_edit.html', {'post': post})
            else:
                return render(request, 'posts.html', {'post': post})

        elif request.method == 'POST':
            post_fields = ['title', 'body']
            for field in post_fields:
                if field in request.POST and request.POST[field] != '':
                    setattr(post, field, request.POST[field])
            post.updated_at = timezone.now()
            post.save()
            return redirect('get_all_posts')  # Redirect to the list of posts after editing

        elif request.method == 'DELETE':
            post.delete()
            return redirect('get_all_posts')  # Redirect to the list of posts after deleting

    return HttpResponse("You should be logged in to delete/edit a post", status=403)


@api_view(['GET'])
def search_post(request):
    query_post_name = request.GET.get('post_name', '')

    posts = Post.objects.filter(title__icontains=query_post_name) | Post.objects.filter(body__icontains=query_post_name)

    serializer = PostSerializer(posts, many=True)  
    return render(request, 'posts.html', {'posts': serializer.data})


@api_view(['GET'])
def like_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_id)

        # Check if the user has already liked this post
        like_instance = Like.objects.filter(user=request.user, post=post).first()
        
        if like_instance:
            # If the like exists, delete it
            like_instance.delete()
            return redirect('get_all_posts') 

        # If the like does not exist, create a new like
        Like.objects.create(user=request.user, post=post)
        return redirect('get_all_posts') 

    return HttpResponse("You should be logged in to like/unlike a post", status=403)


@api_view(['POST'])
def comment_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_id)
        comment_body = request.POST.get('body', '')

        if comment_body:
            Comment.objects.create(post=post, author=request.user, body=comment_body)
            return redirect('get_all_posts')  

    return HttpResponse("You should be logged in to comment on a post", status=403)



@api_view(['GET', 'POST'])
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author != request.user:
        return HttpResponse("You do not have permission to edit this comment.", status=403)

    if request.method == 'POST':
        body = request.POST.get('body')
        if body:
            comment.body = body
            comment.save()
            return redirect('get_all_posts')  

    return render(request, 'edit_comment.html', {'comment': comment})


@api_view(['POST'])
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()

    return redirect('get_all_posts')