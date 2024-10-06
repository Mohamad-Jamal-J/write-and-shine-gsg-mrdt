from abc import ABC


class MessageHandlerFactory(ABC):

    @staticmethod
    def get_handler(app_name: str) -> 'MessageHandler':
        """
        Get a MessageHandler instance for the specified app.

        Args:
            app_name (str): The name of the app (e.g., 'accounts', 'profiles').

        Returns:
            MessageHandler: An instance of MessageHandler initialized with app-specific messages.

        Raises:
            ValueError: If the app name is unknown or messages cannot be loaded.
        """
        success_messages, error_messages = MessageHandlerFactory.load_messages(app_name)
        return MessageHandler(success_messages, error_messages)

    @staticmethod
    def load_messages(app_name: str) -> tuple:
        """
        Load the success and error messages for the specified app.

        Args:
            app_name (str): The name of the app whose messages are to be loaded.

        Returns:
            tuple: A tuple containing success messages and error messages.

        Raises:
            ValueError: If the app name is unknown or messages cannot be found.
        """
        if app_name == 'accounts':
            from accounts.messages import SUCCESS_MESSAGES, ERROR_MESSAGES
        elif app_name == 'profiles':
            from profiles.messages import SUCCESS_MESSAGES, ERROR_MESSAGES
        # elif app_name == 'posts':
        #     from posts.messages import SUCCESS_MESSAGES, ERROR_MESSAGES
        # elif app_name == 'interactions':
        #     from interactions.messages import SUCCESS_MESSAGES, ERROR_MESSAGES
        # elif app_name == 'search':
        #     from interactions.messages import SUCCESS_MESSAGES, ERROR_MESSAGES
        else:
            raise ValueError(f"Unknown app: {app_name}")
        return SUCCESS_MESSAGES, ERROR_MESSAGES


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
