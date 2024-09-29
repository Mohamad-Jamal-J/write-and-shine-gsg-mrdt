from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import api_view

from posts.models import  Post
from interactions.models import Comment, Like, Post



@api_view(['GET'])
def like_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_id)

        # Check if the user has already liked this post
        like_instance = Like.objects.filter(user=request.user, post=post).first()
        
        if like_instance:
            # If the like exists, delete it
            like_instance.delete()
            return redirect('get_posts') 

        # If the like does not exist, create a new like
        Like.objects.create(user=request.user, post=post)
        return redirect('get_posts') 

    return HttpResponse("You should be logged in to like/unlike a post", status=403)


@api_view(['POST'])
def comment_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_id)
        comment_body = request.POST.get('body', '')

        if comment_body:
            Comment.objects.create(post=post, author=request.user, body=comment_body)
            return redirect('get_posts')  

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
            return redirect('get_posts')  

    return render(request, 'edit_comment.html', {'comment': comment})


@api_view(['POST'])
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()

    return redirect('get_posts')
