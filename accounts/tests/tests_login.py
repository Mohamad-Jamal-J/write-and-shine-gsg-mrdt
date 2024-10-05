from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from test_helpers import assert_message, assert_redirect
from ..messages import message_handler


class LoginTests(TestCase):
    def setUp(self):
        """Set up a test client and user for testing."""
        self.client = Client()
        self.User = get_user_model()
        self.user_data = {
            'name': 'Test User',
            'email': 'testuser@ws.com',
            'password': 'passwordTest!'
        }

        self.User.objects.create_user(**self.user_data)

    def test_login_success(self):
        """Test successful login."""
        response = self.client.post(reverse('login_api'), {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        assert_redirect(response, 'get_posts')
        expected_message = message_handler.get('login_successful', False)
        assert_message(response, expected_message)

    def test_login_wrong_password(self):
        """Test login with wrong password."""
        response = self.client.post(reverse('login_api'), {
            'email': self.user_data['email'],
            'password': 'WrongPassword!'
        })

        expected_message = message_handler.get('wrong_password')
        assert_message(response, expected_message)

    def test_login_missing_password(self):
        """Test login with missing password."""
        response = self.client.post(reverse('login_api'), {
            'email': self.user_data['email'],
            'password': ''
        })

        expected_message = message_handler.get('password_required')
        assert_message(response, expected_message)

    def test_login_invalid_email_format(self):
        """Test login with invalid email format."""
        response = self.client.post(reverse('login_api'), {
            'email': 'invalid-email',
            'password': 'passwordTest!'
        })

        expected_message = message_handler.get('invalid_email_format')
        assert_message(response, expected_message)

    def test_login_already_logged_in(self):
        """Test login when already logged in."""
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.post(reverse('login_api'), {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        assert_redirect(response, 'get_posts')
        expected_message = message_handler.get('already_logged_in', name=self.user_data['name'])
        assert_message(response, expected_message)

    def test_login_wrong_request_method(self):
        """Test sending a non-POST request to the login API."""
        response = self.client.delete(reverse('login_api'))

        expected_message = message_handler.get('wrong_request', expected=['POST', 'GET'], received='DELETE')
        assert_message(response, expected_message)
