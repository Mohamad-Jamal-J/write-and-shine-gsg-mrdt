from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
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

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login_api'))

        expected_message = message_handler.get('logged_out', is_error=False)
        messages = list(get_messages(response.wsgi_request))
        self.assertGreater(len(messages), 0)
        self.assertEqual(str(messages[0]), expected_message)

    def test_logout_not_logged_in(self):
        """Test logout when not logged in."""
        response = self.client.get(reverse('logout_api'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login_api'))

        expected_message = message_handler.get('not_logged')
        messages = list(get_messages(response.wsgi_request))
        self.assertGreater(len(messages), 0)
        self.assertEqual(str(messages[0]), expected_message)

    def test_logout_wrong_request_method(self):
        """Test sending a non-POST request to the logout API."""
        self.User.objects.create_user(**self.user_data)
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.delete(reverse('logout_api'))

        expected_message = message_handler.get('wrong_request', expected=['GET'], received='DELETE')
        messages = list(get_messages(response.wsgi_request))
        self.assertGreater(len(messages), 0)
        self.assertEqual(str(messages[0]), expected_message)
