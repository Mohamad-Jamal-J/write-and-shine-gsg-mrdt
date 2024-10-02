from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from profiles.models import Profile
from ..messages import get_feedback_message


class DeleteAccountTests(TestCase):
    def setUp(self):
        """Set up a test client, user, and profile for testing."""
        self.client = Client()
        self.User = get_user_model()
        self.user_data = {
            'name': 'Test User',
            'email': 'testuser@ws.com',
            'password': 'passwordTest!'
        }
        # Create user and profile
        self.user = self.User.objects.create_user(**self.user_data)
        self.profile = Profile.objects.create(user=self.user)

        self.delete_account_url = reverse('delete_account_api')

    def test_delete_account_success(self):
        """Test successful account deletion."""
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.delete(self.delete_account_url)
        messages = list(response.context['messages'])

        expected_message = get_feedback_message('delete_successful', is_error=False)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), expected_message)

        self.assertFalse(self.User.objects.filter(email=self.user_data['email']).exists())

    def test_delete_profile_after_account_deletion(self):
        """Test that the profile is deleted when the account is deleted."""
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        self.client.delete(self.delete_account_url)

        self.assertFalse(Profile.objects.filter(user=self.user).exists())
#
    def test_delete_account_not_logged_in(self):
        """Test trying to delete account when not logged in."""
        response = self.client.delete(self.delete_account_url)
        messages = list(response.context['messages'])

        expected_message = get_feedback_message('not_logged')

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), expected_message)

    def test_delete_account_wrong_request_method(self):
        """Test trying to delete account with a non-DELETE request method."""
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.get(self.delete_account_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('get_posts'))
