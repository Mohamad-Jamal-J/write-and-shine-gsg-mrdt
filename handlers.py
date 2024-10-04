class MessageHandler:
    def __init__(self, success_messages: dict, error_messages: dict):
        """
        Initialize the MessageHandler with success and error messages.

        Args:
            success_messages (dict): Dictionary of success messages.
            error_messages (dict): Dictionary of error messages.
        """
        self.success_messages = success_messages
        self.error_messages = error_messages

    def get(self, message_key: str, is_error=True, **kwargs) -> str:
        """
        Returns the corresponding message (success or error), with optional placeholders.

        Args:
            message_key (str): The message key from success or error dictionaries.
            is_error (bool): True for error message, False for success message.
            **kwargs: Dynamic values to be inserted into the message.

        Returns:
            str: The formatted message.
        """
        unknown = 'Unknown error.'
        message = (
            self.error_messages.get(message_key, unknown) if is_error
            else self.success_messages.get(message_key, unknown)
        )

        if kwargs:
            try:
                message = message.format(**kwargs)
            except KeyError as e:
                return f'Error formatting message: missing placeholder {str(e)}'
        return message
