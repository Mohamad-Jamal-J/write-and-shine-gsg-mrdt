from handlers import MessageHandler

SUCCESS_MESSAGES = {
    'profile_created': 'Profile created successfully.',
    'profile_updated': 'Profile updated successfully.',
    'profile_deleted': 'Profile deleted successfully.',
}

ERROR_MESSAGES = {
    # request method - related error messages
    'wrong_request': 'Request method not allowed. Expected {expected}, but received {received}',

    'profile_not_found': 'No profile found for {id}'
}


message_handler = MessageHandler(SUCCESS_MESSAGES, ERROR_MESSAGES)
