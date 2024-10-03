from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .repository import ProfileRepository
from django.shortcuts import render
from .messages import get_feedback_message


def index(request):
    return render(request, 'profiles/profile.html')


@login_required
def create_or_update_profile(request):
    """
    Handle the creation or update of a user's profile.
    """
    if request.method != 'POST':
        error_message = get_feedback_message('invalid_request_method', expected='POST')
        return JsonResponse({'error': error_message}, status=400)

    user = request.user
    bio = request.POST.get('bio', '')
    education = request.POST.get('education', '')
    profile_picture = request.FILES.get('profile_picture')

    response = ProfileRepository.create_or_update_profile(
        user=user,
        bio=bio,
        education=education,
        profile_picture=profile_picture
    )

    success_message = get_feedback_message('profile_updated', name=user.name)
    return JsonResponse({'message': success_message}, status=200)


@login_required
def get_profile(request):
    """
    Retrieve the user's profile details.
    """
    user = request.user
    profile = ProfileRepository.get_profile(user)

    if profile is None:
        error_message = get_feedback_message('profile_not_found', name=user.name)
        return JsonResponse({'error': error_message}, status=404)

    profile_data = {
        'bio': profile.bio,
        'education': profile.education,
        'profile_picture': profile.profile_picture.url if profile.profile_picture else None
    }

    success_message = get_feedback_message('profile_fetched', name=user.name)
    return JsonResponse({'message': success_message, 'profile': profile_data}, status=200)


@login_required
def delete_profile(request):
    """
    Handle the deletion of a user's profile.
    """
    if request.method != 'DELETE':
        error_message = get_feedback_message('invalid_request_method', expected='DELETE')
        return JsonResponse({'error': error_message}, status=400)

    user = request.user
    response = ProfileRepository.delete_profile(user)

    success_message = get_feedback_message('profile_deleted', name=user.name)
    return JsonResponse({'message': success_message}, status=200)
