SUCCESS_MESSAGES = {
    'account_created': 'Account created successfully.',
    'logged_out': 'Logout successful.',
    'login_successful': 'Login successful.',
    'delete_successful': 'Account was deleted successfully.',
    'password_changed': 'Password was changed successfully.'
}

ERROR_MESSAGES = {
    # request method - related error messages
    'wrong_request': 'Request method not allowed. Expected {expected}, but received {received}',

    # sign in/up related error messages
    'already_logged_in': 'Already logged in as {name}',
    'account_not_found': 'No account associated with the provided email was found.',
    'wrong_password': 'Wrong password, please try again.',
    'not_logged': 'No user is currently logged in.',

    # Registration and login related messages:
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
    'password_special': 'Password should have at least one special character (e.g. !,@,#,$, etc..).',
    'same_password': 'The new password should be different than the old password.'
}


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
