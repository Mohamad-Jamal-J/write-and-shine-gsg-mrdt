from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from test_helpers import assert_message, assert_redirect
from ..messages import message_handler


class LogoutTests(TestCase):
    def setUp(self):
        """Set up a test client and user for testing."""
        self.client = Client()
        self.User = get_user_model()
        self.user_data = {
            'name': 'Test User',
            'email': 'testuser@ws.com',
            'password': 'passwordTest!'
        }

    def test_logout_success(self):
        """Test successful logout."""
        self.User.objects.create_user(**self.user_data)
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.get(reverse('logout_api'))

        assert_redirect(response, 'login_api')
        expected_message = message_handler.get('logged_out', is_error=False)
        assert_message(response, expected_message)

    def test_logout_not_logged_in(self):
        """Test logout when not logged in."""
        response = self.client.get(reverse('logout_api'))

        assert_redirect(response, 'login_api')
        expected_message = message_handler.get('not_logged')
        assert_message(response, expected_message)

    def test_logout_wrong_request_method(self):
        """Test sending a non-POST request to the logout API."""
        self.User.objects.create_user(**self.user_data)
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.delete(reverse('logout_api'))

        assert_redirect(response, 'login_api')
        expected_message = message_handler.get('wrong_request', expected=['GET'], received='DELETE')
        assert_message(response, expected_message)
