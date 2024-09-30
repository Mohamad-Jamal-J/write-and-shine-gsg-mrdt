from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .messages import get_feedback_message
from .repository import AccountRepository
from django.http import HttpResponse
from django.shortcuts import render
from string import punctuation
import re

User = get_user_model()


def index(request):
    return render(request, 'accounts/index.html')


@csrf_exempt  # this will be deleted when we connect the front and back
def signup_api(request) -> HttpResponse:
    """
    Handles user signup as an API endpoint.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Contains success or error message.
    """
    # if user is already logged in, return an error and redirect them to the home page
    error_message = check_authenticated(request)
    if error_message:
        return HttpResponse(error_message, status=403)

    error_message = validate_request_method(request, 'POST')
    if error_message:
        return HttpResponse(error_message, status=405)

    received_data = request.POST
    name = received_data.get('name').strip()
    email = received_data.get('email').strip().lower()
    password = received_data.get('password')

    # check for errors in the input.
    error_message = check_for_invalid_inputs(name, email, password)
    if error_message:
        return HttpResponse(error_message, status=400)

    # check if the email is already used or not in our system.
    if AccountRepository.does_user_exists(email):
        error_message = get_feedback_message('email_exist')
        return HttpResponse(error_message, status=409)

    # create the account.
    if AccountRepository.create_account(name, email, password):
        success_message = get_feedback_message('account_created', False)
        return HttpResponse(success_message, status=201)

    error_message = get_feedback_message('')
    return HttpResponse(error_message, status=500)


@csrf_exempt
def login_api(request) -> HttpResponse:
    """
    Handles user login as an API endpoint.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Contains success or error message.
    """
    error_message = check_authenticated(request)
    if error_message:
        return HttpResponse(error_message, status=403)

    error_message = validate_request_method(request, 'POST')
    if error_message:
        return HttpResponse(error_message, status=405)

    received_data = request.POST
    email = received_data.get('email').strip().lower()
    password = received_data.get('password')

    # Validate email format
    error_message = validate_email(email)
    if error_message:
        return HttpResponse(error_message, status=400)

    # Validate password presence
    error_message = validate_password(password, False)
    if error_message:
        return HttpResponse(error_message, status=400)

    # Attempt to authenticate the user
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        success_message = get_feedback_message('login_successful', False)
        return HttpResponse(success_message, status=200)

    error_message = get_feedback_message('wrong_password')
    return HttpResponse(error_message, status=401)


@csrf_exempt
def logout_api(request) -> HttpResponse:
    """
    Handles user logout as an API endpoint.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Contains success or error message.
    """
    if not request.user.is_authenticated:
        error_message = get_feedback_message('not_logged')
        return HttpResponse(error_message, status=401)

    error_message = validate_request_method(request, 'POST')
    if error_message:
        return HttpResponse(error_message, status=405)

    logout(request)
    success_message = get_feedback_message('logged_out', False)
    return HttpResponse(success_message, status=200)


@csrf_exempt
def delete_account_api(request):
    """
    Handles user account deletion as an API endpoint.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Contains success or error message.
    """
    if not request.user.is_authenticated:
        error_message = get_feedback_message('not_logged')
        return HttpResponse(error_message, status=401)

    user = request.user
    error_message = validate_request_method(request, 'DELETE')
    if error_message:
        return HttpResponse(error_message, status=405)

    return AccountRepository.delete_account(user)


@csrf_exempt
def change_password_api(request):
    """
    Handles password change as an API endpoint.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Contains success or error message.
    """
    if not request.user.is_authenticated:
        error_message = get_feedback_message('not_logged')
        return HttpResponse(error_message, status=401)

    user = request.user
    expected_old_password = user.password
    error_message = validate_request_method(request, 'POST')
    if error_message:
        return HttpResponse(error_message, status=405)

    received_data = request.POST
    old_password = received_data.get('old_password')
    new_password = received_data.get('new_password')
    if not check_password(old_password, expected_old_password):
        error_message = get_feedback_message('wrong_password')
        return HttpResponse(error_message, status=401)

    error_message = validate_password(new_password)
    if error_message:
        return HttpResponse(error_message, status=400)

    if new_password == old_password:
        error_message = get_feedback_message('same_password')
        return HttpResponse(error_message, status=400)

    return AccountRepository.update_password(new_password, user)


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
        return get_feedback_message('already_logged_in', name=request.user.name)
    return None


def validate_request_method(request, expected_method):
    """
    Validates that the HTTP request method matches the expected method.

    Args:
        request (HttpRequest): The HTTP request object containing method information.
        expected_method (str): The expected HTTP method (e.g., 'POST', 'GET').

    Returns:
        str: A feedback message indicating a method mismatch, or None if the method matches the expected one.
    """
    if request.method != expected_method:
        return get_feedback_message('wrong_request', expected=expected_method, received=request.method)
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
        return get_feedback_message('name_required')

    email_error = validate_email(email)
    if email_error:
        return email_error

    password_error = validate_password(password)
    if password_error:
        return password_error

    return ''


def validate_email(email: str) -> str:
    """
    Validates the given email address based on its format.

    Args:
        email (str): The email address to be validated.

    Returns:
        str: An error message if the email is invalid, or an empty string if valid.
    """
    if not email:
        return get_feedback_message('email_required')

    email_pattern = r'^[a-z0-9_.+-]+@[a-z0-9-]+\.[a-z0-9-.]+$'
    if not re.match(email_pattern, email):
        return get_feedback_message('invalid_email_format')
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
        return get_feedback_message('password_required')

    if len(password) < 8:
        return get_feedback_message('password_length')

    if sign_up_checks:
        if not re.search(r'[A-Z]', password):
            return get_feedback_message('password_uppercase')

        if not re.search(f"[{re.escape(punctuation)}]", password):
            return get_feedback_message('password_special')

    return ''
