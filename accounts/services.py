from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from .messages import get_feedback_message
from django.http import HttpResponse

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
        success_message = get_feedback_message('delete_successful', False)
        return HttpResponse(success_message, status=200)

    # I'll get back to this method once we agree on the update functionality with the front
    # @staticmethod
    # def update_name(user, new_name: str):
    #     """
    #     Updates the user's name in the system.
    #
    #     Args:
    #         user: The user whose name is being updated.
    #         new_name (str): The new name to be set.
    #
    #     Returns:
    #         HttpResponse: A success message after the name change.
    #     """
    #     user.name = new_name
    #     user.save()
    #     success_message = get_feedback_message('name_updated', False)
    #     return HttpResponse(success_message, status=200)

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
        success_message = get_feedback_message('password_changed', False)
        user.save()
        return HttpResponse(success_message, status=200)

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
