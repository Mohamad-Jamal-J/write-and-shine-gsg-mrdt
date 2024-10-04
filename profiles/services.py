from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Profile
from .messages import message_handler
User = get_user_model()


class ProfileService:
    @staticmethod
    def get_profile(user_id):
        """
        Retrieves the profile associated with the given user.

        Args:
            user_id: The user id whose profile is being retrieved.

        Returns:
            Profile: The user's profile.
        """
        try:
            user = get_object_or_404(User, id=user_id)
            return Profile.objects.get(user=user)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create_default_profile(user):
        """
        Creates or updates a profile with the provided information.

        Args:
            user: The user to whom the profile belongs.

        Returns:
            HttpResponse: A success message after profile creation or update.
        """
        return ProfileService.create_or_update_profile(user)

    @staticmethod
    def create_or_update_profile(user, headline='', bio='', education='', profile_picture=None):
        """
        Creates or updates a profile with the provided information.

        Args:
            user: The user to whom the profile belongs.
            headline (str): The user's headline.
            bio (str): The user's bio.
            education (str): The user's educational background.
            profile_picture (File): The user's profile picture.

        Returns:
            HttpResponse: A success message after profile creation or update.
        """
        profile, created = Profile.objects.get_or_create(user=user)

        if headline:
            profile.headline = headline
        if bio:
            profile.bio = bio
        if education:
            profile.education = education
        if profile_picture:
            profile.profile_picture = profile_picture

        profile.save()

        if created:
            success_message = message_handler.get('profile_created', False)
        else:
            success_message = message_handler.get('profile_updated', False)

        return HttpResponse(success_message, status=200)

    @staticmethod
    def delete_profile(user):
        """
        Deletes the profile associated with the given user.

        Args:
            user: The user whose profile is being deleted.

        Returns:
            HttpResponse: A success message after profile deletion.
        """
        profile = get_object_or_404(Profile, user=user)
        profile.delete()
        success_message = message_handler.get('profile_deleted', False)
        return HttpResponse(success_message, status=200)
