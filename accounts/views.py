from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.http import JsonResponse
import re
from string import punctuation
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password

User = get_user_model()

SUCCESS_MESSAGES = {
    'account_created': 'Account created successfully.',
    'logged_out': 'Logout successful.',
    'login_successful': 'Login successful.'
}
ERROR_MESSAGES = {
    # sign in/up related error messages
    'already_logged_in': 'Already logged in as {name}',
    'account_not_found': 'No Account associated with the provided email was found.',
    'wrong_request': 'Wrong request method. Expected POST, but received {method}',
    'wrong_password': 'Wrong password, please try again.',
    'not_logged': 'No user is currently logged in.',

    # name-related error messages
    'name_required': 'name is required.',

    # Email-related error messages
    'email_required': 'Email field is required.',
    'invalid_email_format': 'Invalid email format.',
    'email_exist': 'The provided email is used for another account.',

    # Password-related error messages
    'password_required': 'Password field is required.',
    'password_length': 'Password should have at least 8 characters.',
    'password_uppercase': 'Password should have at least one uppercase letter.',
    'password_special': 'Password should have at least one special character (e.g. !,@,#,$, etc..).'
}


def index(request):
    return render(request, 'accounts/index.html')


@csrf_exempt  # this will be deleted when we connect the front and back
def signup_api(request):
    """
    Handles user signup as an API endpoint.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: Contains success or error message.
    """
    data = {
        'data': None,
        'error': None
    }

    # if user is already logged in, return an error and redirect them to the home page
    if request.user.is_authenticated:
        data['error'] = get_feedback_message('already_logged_in', name=request.user.name)
        return JsonResponse(data, status=400)

    if request.method == 'POST':
        received_data = request.POST
        name = received_data.get('name')
        email = received_data.get('email')
        password = received_data.get('password')

        # check for errors in the input.
        data['error'] = check_for_invalid_inputs(name, email, password)
        if data['error']:
            return JsonResponse(data, status=400)

        # check if the email is already used or not in our system.
        if user_exists(email):
            data['error'] = get_feedback_message('email_exist')
            return JsonResponse(data, status=400)

        # create the account.
        if create_account(name, email, password):
            data['data'] = get_feedback_message('account_created', is_error=False)
            status = 200
        else:
            data['error'] = get_feedback_message('')
            status = 400
        return JsonResponse(data, status=status)

    data['error'] = get_feedback_message('wrong_request', method=request.method)
    return JsonResponse(data, status=400)


@csrf_exempt
def login_api(request):
    """
    Handles user login as an API endpoint.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: Contains success or error message.
    """
    data = {
        'data': None,
        'error': None
    }
    if request.user.is_authenticated:
        data['error'] = get_feedback_message('already_logged_in', name=request.user.name)
        return JsonResponse(data, status=400)

    if request.method == 'POST':
        received_data = request.POST
        email = received_data.get('email')
        password = received_data.get('password')

        # Validate email format
        data['error'] = validate_email(email)
        if data['error']:
            return JsonResponse(data, status=400)

        # Validate password presence
        if not password:
            data['error'] = get_feedback_message('password_required')
            return JsonResponse(data, status=400)

        # Attempt to authenticate the user using email as name
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            data['data'] = get_feedback_message('login_successful', is_error=False)
            return JsonResponse(data, status=200)
        else:
            data['error'] = get_feedback_message('wrong_password')
            return JsonResponse(data, status=400)

    data['error'] = get_feedback_message('wrong_request', method=request.method)
    return JsonResponse(data, status=400)


@csrf_exempt
def logout_api(request):
    """
    Handles user logout as an API endpoint.

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: Contains success or error message.
    """
    data = {
        'data': None,
        'error': None
    }

    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            data['data'] = get_feedback_message('logged_out', is_error=False)
            return JsonResponse(data, status=200)
        else:
            data['error'] = get_feedback_message('not_logged')
            return JsonResponse(data, status=400)

    data['error'] = get_feedback_message('wrong_request', method=request.method)
    return JsonResponse(data, status=400)


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
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_pattern, email):
        return get_feedback_message('invalid_email_format')

    return ''


def validate_password(password: str) -> str:
    """
    Validates the given password based on various criteria.

    Args:
        password (str): The password to be validated.

    Returns:
        str: An error message if the password is invalid, or an empty string if valid.
    """
    if not password:
        return get_feedback_message('password_required')

    if len(password) < 8:
        return get_feedback_message('password_length')

    if not re.search(r'[A-Z]', password):
        return get_feedback_message('password_uppercase')

    if not re.search(f"[{re.escape(punctuation)}]", password):
        return get_feedback_message('password_special')

    return ''


def get_feedback_message(message_key: str, is_error=True, **kwargs) -> str:
    """
    Returns a corresponding error message based on the error type, with optional
    placeholders for dynamic values.

    Args:
        message_key (str): The message key from SUCCESS_MESSAGES or ERROR_MESSAGES.
        is_error (bool): Optional param - The type of message is error when True, and feedback otherwise.
        **kwargs: Dynamic values to be inserted into the message.

    Returns:
        str: The corresponding message with placeholders filled.
    """
    unknown = 'Unknown error.'
    if is_error:
        message = ERROR_MESSAGES.get(message_key, unknown)
    else:
        message = SUCCESS_MESSAGES.get(message_key, unknown)
    if kwargs:
        try:
            message = message.format(**kwargs)
        except KeyError as e:
            return f'Error formatting message: missing placeholder {str(e)}'
    return message


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
