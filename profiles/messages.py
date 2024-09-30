SUCCESS_MESSAGES = {
    'profile_created': 'Profile created successfully.',
    'profile_updated': 'Profile updated successfully.',
    'profile_deleted': 'Profile deleted successfully.',
}

ERROR_MESSAGES = {
    # request method - related error messages
    'wrong_request': 'Request method not allowed. Expected {expected}, but received {received}',
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
