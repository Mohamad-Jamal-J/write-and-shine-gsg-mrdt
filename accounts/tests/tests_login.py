from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..messages import get_feedback_message


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

    def test_login_success(self):
        """Test successful login."""
        self.User.objects.create_user(**self.user_data)
        response = self.client.post(reverse('login_api'), {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('get_posts'))

    def test_login_wrong_password(self):
        """Test login with wrong password."""
        self.User.objects.create_user(**self.user_data)
        response = self.client.post(reverse('login_api'), {
            'email': self.user_data['email'],
            'password': 'WrongPassword!'
        })
        messages = list(response.context['messages'])

        expected_message = get_feedback_message('wrong_password')

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), expected_message)

    def test_login_missing_password(self):
        """Test login with missing password."""
        self.User.objects.create_user(**self.user_data)
        response = self.client.post(reverse('login_api'), {
            'email': self.user_data['email'],
            'password': ''
        })
        messages = list(response.context['messages'])

        expected_message = get_feedback_message('password_required')

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), expected_message)

    def test_login_invalid_email_format(self):
        """Test login with invalid email format."""
        response = self.client.post(reverse('login_api'), {
            'email': 'invalid-email',
            'password': 'passwordTest!'
        })
        messages = list(response.context['messages'])

        expected_message = get_feedback_message('invalid_email_format')

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), expected_message)

    def test_login_already_logged_in(self):
        """Test login when already logged in."""
        user = self.User.objects.create_user(**self.user_data)
        self.client.force_login(user)
        response = self.client.post(reverse('login_api'), {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('get_posts'))

    def test_login_wrong_request_method(self):
        """Test sending a non-POST request to the login API."""
        response = self.client.delete(reverse('login_api'))
        messages = list(response.context['messages'])

        expected_message = get_feedback_message('wrong_request', expected=['POST', 'GET'], received='DELETE')

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), expected_message)
