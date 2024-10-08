from django.contrib.auth.decorators import login_required
from django.urls import reverse
from posts.views import get_user_posts_raw
from .services import ProfileService
from django.shortcuts import render, redirect
from .messages import message_handler
from django.contrib import messages


@login_required
def create_or_update_profile(request):
    """
    Handle the creation or update of a user's profile.
    """
    user = request.user
    if request.method != 'POST':
        error_message = message_handler.get('invalid_request_method', expected='POST')
        messages.error(request, error_message)
        return redirect('get_profile', user.id)

    headline = request.POST.get('headline', '')
    bio = request.POST.get('bio', '')
    education = request.POST.get('education', '')
    profile_picture = request.FILES.get('profile_picture')

    response = ProfileService.create_or_update_profile(
        user=user,
        headline=headline,
        bio=bio,
        education=education,
        profile_picture=profile_picture
    )
    # success_message = messages.get_messages(response)
    # messages.success(response, success_message)
    return redirect('get_profile', user.id)


def get_profile(request, user_id: int):
    """
    Retrieve the user's profile details.
    """
    user_posts_data = get_user_posts_raw(request, user_id)

    user = user_posts_data.get('user', {})
    posts = user_posts_data.get('posts', [])

    profile = ProfileService.get_profile(user_id)

    if profile is None:
        error_message = message_handler.get('profile_not_found', id=user_id)
        messages.error(request, error_message)
        return redirect(reverse('get_posts'))

    profile_data = {
        'id': user.get('id'),
        'name': user.get('name'),
        'headline': profile.headline,
        'bio': profile.bio,
        'education': profile.education,
        'profile_picture': profile.profile_picture.url,
        'is_owner': request.user.is_authenticated and request.user.id == user_id,
        'posts': posts
    }
    return render(request, 'user.html', profile_data)
