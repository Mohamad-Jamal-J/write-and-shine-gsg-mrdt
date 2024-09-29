from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .messages import get_feedback_message
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
    if request.user.is_authenticated:
        error_message = get_feedback_message('already_logged_in', name=request.user.name)
        return HttpResponse(error_message, status=403)

    if request.method == 'POST':
        received_data = request.POST
        name = received_data.get('name').strip()
        email = received_data.get('email').strip().lower()
        password = received_data.get('password')

        # check for errors in the input.
        error_message = check_for_invalid_inputs(name, email, password)
        if error_message:
            return HttpResponse(error_message, status=400)

        # check if the email is already used or not in our system.
        if user_exists(email):
            error_message = get_feedback_message('email_exist')
            return HttpResponse(error_message, status=409)

        # create the account.
        if create_account(name, email, password):
            error_message = get_feedback_message('account_created', is_error=False)
            status = 201
        else:
            error_message = get_feedback_message('')
            status = 500
        return HttpResponse(error_message, status=status)

    error_message = get_feedback_message('wrong_request', method=request.method)
    return HttpResponse(error_message, status=405)


@csrf_exempt
def login_api(request) -> HttpResponse:
    """
    Handles user login as an API endpoint.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Contains success or error message.
    """
    if request.user.is_authenticated:
        error_message = get_feedback_message('already_logged_in', name=request.user.name)
        return HttpResponse(error_message, status=403)

    if request.method == 'POST':
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
            success_message = get_feedback_message('login_successful', is_error=False)
            return HttpResponse(success_message, status=200)
        else:
            error_message = get_feedback_message('wrong_password')
            return HttpResponse(error_message, status=401)

    error_message = get_feedback_message('wrong_request', method=request.method)
    return HttpResponse(error_message, status=405)


@csrf_exempt
def logout_api(request) -> HttpResponse:
    """
    Handles user logout as an API endpoint.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Contains success or error message.
    """
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            success_message = get_feedback_message('logged_out', is_error=False)
            return HttpResponse(success_message, status=200)
        else:
            error_message = get_feedback_message('not_logged')
            return HttpResponse(error_message, status=401)

    error_message = get_feedback_message('wrong_request', method=request.method)
    return HttpResponse(error_message, status=405)


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
    email_pattern = r'^[a-z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_pattern, email):
        return get_feedback_message('invalid_email_format')

    return ''


def validate_password(password: str, sign_up_checks: bool = True) -> str:
    """
    Validates the given password based on various criteria.

    Args:
        password (str): The password to be validated.
        sign_up_checks (bool): Whether to make extra validations for string password or not.

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


def user_exists(email: str) -> bool:
    """
     Checks if a user with the given email is already in the system.

     Args:
         email (str): The email to check.

     Returns:
         bool: True if a user is found, False otherwise.
     """
    return User.objects.filter(email=email).exists()


def create_account(name: str, email: str, password: str) -> User:
    """
     Creates a new user account in the system's database.

     Args:
         name (str): The user name.
         email (str): The email.
         password (str): The password.

     Returns:
         User: A user object if the account is created, or an empty string if not.
     """
    user = User.objects.create(
        name=name,
        email=email,
        password=make_password(password)
    )
    user.save()
    return user
