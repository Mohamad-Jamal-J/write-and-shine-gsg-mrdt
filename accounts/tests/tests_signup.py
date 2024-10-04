from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from profiles.models import Profile
from accounts.models import User
from ..messages import message_handler


class SignupTests(TestCase):
    def setUp(self):
        """Set up a test client and user for testing."""
        self.client = Client()
        self.User = get_user_model()
        self.user_data = {
            'name': 'Test User',
            'email': 'testuser@ws.com',
            'password': 'passwordTest!'
        }

    def test_signup_success(self):
        """Test successful signup."""
        response = self.client.post(reverse('signup_api'), self.user_data)

        self.assertTrue(User.objects.filter(email=self.user_data['email']).exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login_api'))

    def test_profile_created_on_signup(self):
        """Test that a profile is created when a user successfully signs up."""
        self.client.post(reverse('signup_api'), self.user_data)

        user = self.User.objects.get(email=self.user_data['email'])
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_signup_email_exists(self):
        """Test signup when email already exists."""
        self.User.objects.create_user(**self.user_data)
        response = self.client.post(reverse('signup_api'), self.user_data)
        messages = list(response.context['messages'])

        expected_message = message_handler.get('email_exist')

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), expected_message)

    def test_signup_email_string_case(self):
        """
        Test signup when email already exists and a variation of string case is entered.
        e.g. upper case variation of the same email
        """
        self.User.objects.create_user(**self.user_data)
        self.user_data['email'] = self.user_data['email'].upper()
        response = self.client.post(reverse('signup_api'), self.user_data)
        messages = list(response.context['messages'])

        expected_message = message_handler.get('email_exist')

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), expected_message)

    def test_signup_invalid_email(self):
        """Test signup with invalid email."""
        invalid_user_data = self.user_data.copy()
        invalid_user_data['email'] = 'invalid-email'
        response = self.client.post(reverse('signup_api'), invalid_user_data)
        messages = list(response.context['messages'])

        expected_message = message_handler.get('invalid_email_format')

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), expected_message)

    def test_signup_missing_name(self):
        """Test signup with missing name."""
        invalid_user_data = self.user_data.copy()
        invalid_user_data['name'] = ''
        response = self.client.post(reverse('signup_api'), invalid_user_data)
        messages = list(response.context['messages'])

        expected_message = message_handler.get('name_required')

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), expected_message)

    def test_signup_short_password(self):
        """Test signup with a short password."""
        invalid_user_data = self.user_data.copy()
        invalid_user_data['password'] = 'Short1!'
        response = self.client.post(reverse('signup_api'), invalid_user_data)
        messages = list(response.context['messages'])

        expected_message = message_handler.get('password_length')

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), expected_message)

    def test_signup_wrong_request_method(self):
        """Test sending a non-POST request to the signup API."""
        response = self.client.delete(reverse('signup_api'))
        messages = list(response.context['messages'])

        expected_message = message_handler.get('wrong_request', expected=['POST', 'GET'], received='DELETE')

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), expected_message)
