from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .messages import message_handler
from django.http import HttpResponse
from profiles.services import ProfileService

User = get_user_model()


class AccountService:
    @staticmethod
    def create_account(name: str, email: str, password: str) -> bool:
        """
        Creates a new user account in the system's database.

        Args:
            name (str): The user's name.
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            User: The created User object.
        """
        user = User.objects.create(
            name=name,
            email=email,
            password=make_password(password)
        )
        user.save()
        ProfileService.create_default_profile(user)
        return True

    @staticmethod
    def delete_account(user):
        """
        Deletes the user account from the system.

        Args:
            user: The user to be deleted.

        Returns:
            HttpResponse: A success message after account deletion.
        """
        user.delete()
        return message_handler.get('delete_successful', False)

    @staticmethod
    def update_password(new_password, user):
        """
        Updates the user's password in the system.

        Args:
            new_password (str): The new password.
            user: The user whose password is being updated.

        Returns:
            HttpResponse: A success message after password change.
        """
        user.set_password(new_password)
        user.save()
        return message_handler.get('password_changed', False)

    @staticmethod
    def does_user_exists(email: str) -> bool:
        """
        Checks if a user with the given email exists in the system.

        Args:
            email (str): The email to check.

        Returns:
            bool: True if a user with the email exists, False otherwise.
        """
        return User.objects.filter(email=email).exists()
