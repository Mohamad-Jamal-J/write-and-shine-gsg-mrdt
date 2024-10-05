from django.contrib.messages import get_messages
from django.urls import reverse


def assert_message(response, expected_message):
    """Helper method to assert the presence and content of messages."""
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) > 0, "No messages were found in the response."
    assert str(messages[0]) == expected_message, f"Expected message '{expected_message}', but got '{str(messages[0])}'."


def assert_redirect(response, expected_url_name, **kwargs):
    """Helper method to assert response redirection."""
    assert response.status_code == 302, f"Expected status code 302, but got {response.status_code}."
    expected_url = reverse(expected_url_name, kwargs=kwargs)
    assert response.url == expected_url, f"Expected redirect to '{expected_url}', but got '{response.url}'."
