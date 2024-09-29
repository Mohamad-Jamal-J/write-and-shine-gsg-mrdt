from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..messages import get_feedback_message


class DeleteAccountTests(TestCase):
    def setUp(self):
        """Set up a test client and a user for testing."""
        self.client = Client()
        self.User = get_user_model()
        self.user_data = {
            'name': 'Test User',
            'email': 'testuser@ws.com',
            'password': 'passwordTest!'
        }
        self.user = self.User.objects.create_user(**self.user_data)
        self.delete_account_url = reverse('delete_account_api')

    def test_delete_account_success(self):
        """Test successful account deletion."""
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.delete(self.delete_account_url)

        expected_message = get_feedback_message('delete_successful', is_error=False)
        self.assertContains(response, expected_message, status_code=200)
        self.assertFalse(self.User.objects.filter(email=self.user_data['email']).exists())

    def test_delete_account_not_logged_in(self):
        """Test trying to delete account when not logged in."""
        response = self.client.delete(self.delete_account_url)

        expected_message = get_feedback_message('not_logged')
        self.assertContains(response, expected_message, status_code=401)

    def test_delete_account_wrong_request_method(self):
        """Test trying to delete account with a non-DELETE request method."""
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.get(self.delete_account_url)

        expected_message = get_feedback_message('wrong_request', expected='DELETE', received='GET')
        self.assertContains(response, expected_message, status_code=405)