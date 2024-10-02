from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..messages import get_feedback_message


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
        messages = list(response.context['messages'])

        expected_message = get_feedback_message('logged_out', is_error=False)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), expected_message)

    def test_logout_not_logged_in(self):
        """Test logout when not logged in."""
        response = self.client.get(reverse('logout_api'))
        messages = list(response.context['messages'])

        expected_message = get_feedback_message('not_logged')

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), expected_message)

    def test_logout_wrong_request_method(self):
        """Test sending a non-POST request to the logout API."""
        self.User.objects.create_user(**self.user_data)
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.delete(reverse('logout_api'))
        messages = list(response.context['messages'])

        expected_message = get_feedback_message('wrong_request', expected=['GET'], received='DELETE')

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), expected_message)
