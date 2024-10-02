from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from ..messages import get_feedback_message


class ChangePasswordTests(TestCase):
    def setUp(self):
        """Set up a test client and user for testing."""
        self.client = Client()
        self.User = get_user_model()
        self.user_data = {
            'name': 'Test User',
            'email': 'testuser@ws.com',
            'password': 'passwordTest!'
        }
        self.user = self.User.objects.create_user(
            name=self.user_data['name'],
            email=self.user_data['email'],
            password=self.user_data['password']
        )
        self.change_password_url = reverse('change_password_api')

    def test_change_password_success(self):
        """Test successfully changing the password."""
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        new_password = 'NewPassword123!'

        response = self.client.post(self.change_password_url, {
            'old_password': self.user_data['password'],
            'new_password': new_password
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('get_posts'))

        # Verify the password was updated
        self.user.refresh_from_db()
        self.assertTrue(check_password(new_password, self.user.password))

    def test_change_password_same_as_old(self):
        """Test trying to change the password to the same old one."""
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.post(self.change_password_url, {
            'old_password': self.user_data['password'],
            'new_password': self.user_data['password']
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('get_posts'))

    def test_change_password_invalid_new_password(self):
        """Test trying to change the password with an invalid new password."""
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        invalid_password = '123'

        response = self.client.post(self.change_password_url, {
            'old_password': self.user_data['password'],
            'new_password': invalid_password
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('get_posts'))

    def test_change_password_incorrect_old_password(self):
        """Test trying to change the password with the wrong old password."""
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.post(self.change_password_url, {
            'old_password': 'WrongPassword123!',
            'new_password': 'NewPassword123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('get_posts'))

    def test_change_password_not_logged_in(self):
        """Test trying to change the password when not logged in."""
        response = self.client.post(self.change_password_url, {
            'old_password': self.user_data['password'],
            'new_password': 'NewPassword123!'
        })
        messages = list(response.context['messages'])

        expected_message = get_feedback_message('not_logged')

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), expected_message)

    def test_change_password_wrong_request_method(self):
        """Test trying to change the password with a non-POST request method."""
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.get(self.change_password_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('get_posts'))
