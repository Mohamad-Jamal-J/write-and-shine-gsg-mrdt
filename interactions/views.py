from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import api_view
from .services import InteractionRepository
from posts.models import Post

@api_view(['GET'])
def like_post(request, post_id):
    """
    Handles liking or unliking a post.

    Args:
        request: The HTTP request object.
        post_id: The ID of the post to like/unlike.

    Returns:
        HttpResponse: Redirect to the post page or error message.
    """
    if request.user.is_authenticated:
        result = InteractionRepository.toggle_like(request.user, post_id)
        if result['success']:
            return redirect('get_posts')
        return HttpResponse(result['message'], status=403)

    messages.error(request, "You should be logged in to like/unlike a post" )
    return redirect('login_api')


@api_view(['POST'])
def comment_post(request, post_id):
    """
    Handles commenting on a post.

    Args:
        request: The HTTP request object.
        post_id: The ID of the post to comment on.

    Returns:
        HttpResponse: Redirect to the post page or error message.
    """
    if request.user.is_authenticated:
        comment_body = request.POST.get('body', '')
        result = InteractionRepository.add_comment(request.user, post_id, comment_body)
        if result['success']:
            return redirect('get_posts')
        return HttpResponse(result['message'], status=400)

    messages.error(request, "You should be logged in to comment on a post")
    return redirect('login_api')


@api_view(['GET', 'POST'])
def edit_comment(request, comment_id):
    """
    Handles editing an existing comment.

    Args:
        request: The HTTP request object.
        comment_id: The ID of the comment to edit.

    Returns:
        HttpResponse: Render edit page or redirect after editing.
    """
    result = InteractionRepository.get_comment(comment_id)
    if not result['success']:
        return HttpResponse(result['message'], status=404)

    comment = result['comment']
    if comment.author != request.user:
        return HttpResponse("You do not have permission to edit this comment.", status=403)

    if request.method == 'POST':
        body = request.POST.get('body')
        if body:
            InteractionRepository.update_comment_body(comment, body)
            return redirect('get_posts')

    return render(request, 'edit_comment.html', {'comment': comment})


@api_view(['POST'])
def delete_comment(request, comment_id):
    """
    Handles deleting a comment.

    Args:
        request: The HTTP request object.
        comment_id: The ID of the comment to delete.

    Returns:
        HttpResponse: Redirect to posts page or error message.
    """
    result = InteractionRepository.get_comment(comment_id)
    if not result['success']:
        return HttpResponse(result['message'], status=404)

    comment = result['comment']
    if comment.author == request.user:
        InteractionRepository.delete_comment(comment)
        return redirect('get_posts')

    return HttpResponse("You do not have permission to delete this comment.", status=403)
