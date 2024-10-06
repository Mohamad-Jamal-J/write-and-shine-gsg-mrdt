from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from .messages import message_handler
from .services import AccountService
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from string import punctuation
import re

User = get_user_model()


def signup_api(request) -> HttpResponse:
    """
    Handles user signup as an API endpoint.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the signup page with success or error message.
    """
    # if user is already logged in, return an error and redirect them to the home page
    error_message = check_authenticated(request)
    if error_message:
        messages.error(request, error_message)
        return redirect(reverse('get_posts'))

    error_message = validate_request_method(request, ['POST', 'GET'])
    if error_message:
        messages.error(request, error_message)
        return render(request, 'accounts/sign_up.html')

    if request.method == 'POST':
        received_data = request.POST
        name = received_data.get('name').strip()
        email = received_data.get('email').strip().lower()
        password = received_data.get('password')
        data = {'name': name,
                'email': email}

        # check for errors in the input.
        error_message = check_for_invalid_inputs(name, email, password)
        if error_message:
            messages.error(request, error_message)
            return render(request, 'accounts/sign_up.html', data)

        # check if the email is already used or not in our system.
        if AccountService.does_user_exists(email):
            error_message = message_handler.get('email_exist')
            messages.error(request, error_message)
            return render(request, 'accounts/sign_up.html', data)

        # create the account.
        if AccountService.create_account(name, email, password):
            success_message = message_handler.get('account_created', False)
            messages.success(request, success_message)
            return redirect('login_api')

        error_message = message_handler.get('')
        messages.error(request, error_message)
    return render(request, 'accounts/sign_up.html')


def login_api(request) -> HttpResponse:
    """
    Handles user login as an API endpoint.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the login page, with success or error message.
    """
    data = {}
    error_message = check_authenticated(request)
    if error_message:
        messages.error(request, error_message)
        return redirect(reverse('get_posts'))

    error_message = validate_request_method(request, ['POST', 'GET'])
    if error_message:
        messages.error(request, error_message)
        return render(request, 'accounts/login.html')

    if request.method == 'POST':
        received_data = request.POST
        email = received_data.get('email').strip().lower()
        password = received_data.get('password')

        data = {'email': email}

        # Validate email format
        error_message = validate_email(email, True)
        if error_message:
            messages.error(request, error_message)
            return render(request, 'accounts/login.html', data)

        # Validate password presence
        error_message = validate_password(password, False)
        if error_message:
            messages.error(request, error_message)
            return render(request, 'accounts/login.html', data)

        # Attempt to authenticate the user
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            success_message = message_handler.get('login_successful', False)
            messages.success(request, success_message)
            return redirect(reverse('get_posts'))

        error_message = message_handler.get('wrong_password')
        messages.error(request, error_message)
    return render(request, 'accounts/login.html', data)


def logout_api(request) -> HttpResponse:
    """
    Handles user logout as an API endpoint.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the login page, with success or error message.
    """
    if not request.user.is_authenticated:
        error_message = message_handler.get('not_logged')
        messages.error(request, error_message)
        return redirect('login_api')

    error_message = validate_request_method(request, ['GET'])
    if error_message:
        messages.error(request, error_message)
        return redirect('login_api')

    logout(request)
    success_message = message_handler.get('logged_out', False)
    messages.success(request, success_message)
    return redirect('login_api')


def delete_account_api(request):
    """
    Handles user account deletion as an API endpoint.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Contains success or error message.
    """
    if not request.user.is_authenticated:
        error_message = message_handler.get('not_logged')
        messages.error(request, error_message)
        return redirect('login_api')

    user = request.user
    error_message = validate_request_method(request, ['DELETE'])
    if error_message:
        messages.error(request, error_message)
        return redirect(reverse('get_profile', kwargs={'user_id': user.id}))

    success_message = AccountService.delete_account(user)
    messages.success(request, success_message)
    return redirect('login_api')


def change_password_api(request):
    """
    Handles password change as an API endpoint.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Contains success or error message.
    """
    if not request.user.is_authenticated:
        error_message = message_handler.get('not_logged')
        messages.error(request, error_message)
        return redirect('login_api')

    user = request.user
    expected_old_password = user.password
    error_message = validate_request_method(request, ['POST'])
    if error_message:
        messages.error(request, error_message)
        return redirect(reverse('get_profile', kwargs={'user_id': user.id}))

    received_data = request.POST
    old_password = received_data.get('old_password')
    new_password = received_data.get('new_password')
    if not check_password(old_password, expected_old_password):
        error_message = message_handler.get('wrong_password')
        messages.error(request, error_message)
        return redirect(reverse('get_profile', kwargs={'user_id': user.id}))

    error_message = validate_password(new_password)
    if error_message:
        messages.error(request, error_message)
        return redirect(reverse('get_profile', kwargs={'user_id': user.id}))

    if new_password == old_password:
        error_message = message_handler.get('same_password')
        messages.error(request, error_message)
        return redirect(reverse('get_profile', kwargs={'user_id': user.id}))

    success_message = AccountService.update_password(new_password, user)
    messages.success(request, success_message)
    return redirect(reverse('get_profile', kwargs={'user_id': user.id}))


def check_authenticated(request):
    """
    Checks if the user making the request is already authenticated.

    Args:
        request (HttpRequest): The HTTP request object containing user information.

    Returns:
        str: A feedback message indicating that the user is already logged in,
             or None if the user is not authenticated.
    """
    if request.user.is_authenticated:
        return message_handler.get('already_logged_in', name=request.user.name)
    return None


def validate_request_method(request, expected_methods):
    """
    Validates that the HTTP request method matches the expected method.

    Args:
        request (HttpRequest): The HTTP request object containing method information.
        expected_methods (list): The expected HTTP methods (e.g., 'POST', 'GET').

    Returns:
        str: A feedback message indicating a method mismatch, or None if the method matches the expected one.
    """
    if request.method not in expected_methods:
        return message_handler.get('wrong_request', expected=expected_methods, received=request.method)
    return None


def check_for_invalid_inputs(name: str, email: str, password: str) -> str:
    """
    Checks for invalid inputs in the name, email, and password fields.

    Args:
        name (str): The name to be validated.
        email (str): The email to be validated.
        password (str): The password to be validated.

    Returns:
        str: An error message if any input is invalid, or an empty string if all are valid.
    """
    if not name:
        return message_handler.get('name_required')

    email_error = validate_email(email)
    if email_error:
        return email_error

    password_error = validate_password(password)
    if password_error:
        return password_error

    return ''


def validate_email(email: str, login_checks: bool = False) -> str:
    """
    Validates the given email address based on its format.

    Args:
        email (str): The email address to be validated.
        login_checks (bool): If True add login validations, otherwise don't.

    Returns:
        str: An error message if the email is invalid, or an empty string if valid.
    """
    if not email:
        return message_handler.get('email_required')

    email_pattern = r'^[a-z0-9_.+-]+@[a-z0-9-]+\.[a-z0-9-.]+$'
    if not re.match(email_pattern, email):
        return message_handler.get('invalid_email_format')

    if login_checks and not AccountService.does_user_exists(email):
        return message_handler.get('account_not_found')
    return ''


def validate_password(password: str, sign_up_checks: bool = True) -> str:
    """
    Validates the given password based on various criteria.

    Args:
        password (str): The password to be validated.
        sign_up_checks (bool): Whether to make extra validations for strong password or not.

    Returns:
        str: An error message if the password is invalid, or an empty string if valid.
    """
    if not password:
        return message_handler.get('password_required')

    if len(password) < 8:
        return message_handler.get('password_length')

    if sign_up_checks:
        if not re.search(r'[A-Z]', password):
            return message_handler.get('password_uppercase')

        if not re.search(f"[{re.escape(punctuation)}]", password):
            return message_handler.get('password_special')

    return ''
