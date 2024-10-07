from handlers import MessageHandlerFactory

SUCCESS_MESSAGES = {
    'post_created': 'Post created successfully.',
    'post_updated': 'Post updated successfully.',
    'post_deleted': 'Post deleted successfully.',
    'tag_removed': 'Tag Removed successfully.',
}

ERROR_MESSAGES = {
    # request method - related error messages
    'invalid_data': 'The post data is invalid.',
    'not_logged': 'You should have an account and be logged in.',
    'no_permission_to_edit': 'You do not have permission to edit or delete this post.',
    'user_not_found': 'No user associated with the provided data was found.',
    'post_not_found': 'No post associated with the provided data was found.',
    'tag_not_found': 'No tag associated with the provided data was found.',
}


message_handler = MessageHandlerFactory.get_handler('posts')
