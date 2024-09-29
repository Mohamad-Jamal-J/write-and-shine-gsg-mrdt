from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..messages import get_feedback_message


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
        expected_message = get_feedback_message('account_created', is_error=False)

        self.assertContains(response, expected_message, status_code=201)

    def test_signup_email_exists(self):
        """Test signup when email already exists."""
        self.User.objects.create_user(**self.user_data)
        response = self.client.post(reverse('signup_api'), self.user_data)

        expected_message = get_feedback_message('email_exist')
        self.assertContains(response, expected_message, status_code=409)

    def test_signup_email_string_case(self):
        """
        Test signup when email already exists and a variation of string case is entered.
        e.g. upper case variation of the same email
        """
        self.User.objects.create_user(**self.user_data)
        self.user_data['email'] = self.user_data['email'].upper()
        response = self.client.post(reverse('signup_api'), self.user_data)

        expected_message = get_feedback_message('email_exist')
        self.assertContains(response, expected_message, status_code=409)

    def test_signup_invalid_email(self):
        """Test signup with invalid email."""
        invalid_user_data = self.user_data.copy()
        invalid_user_data['email'] = 'invalid-email'
        response = self.client.post(reverse('signup_api'), invalid_user_data)

        expected_message = get_feedback_message('invalid_email_format')
        self.assertContains(response, expected_message, status_code=400)

    def test_signup_missing_name(self):
        """Test signup with missing name."""
        invalid_user_data = self.user_data.copy()
        invalid_user_data['name'] = ''
        response = self.client.post(reverse('signup_api'), invalid_user_data)

        expected_message = get_feedback_message('name_required')
        self.assertContains(response, expected_message, status_code=400)

    def test_signup_short_password(self):
        """Test signup with a short password."""
        invalid_user_data = self.user_data.copy()
        invalid_user_data['password'] = 'Short1!'
        response = self.client.post(reverse('signup_api'), invalid_user_data)

        expected_message = get_feedback_message('password_length')
        self.assertContains(response, expected_message, status_code=400)

    def test_signup_wrong_request_method(self):
        """Test sending a non-POST request to the signup API."""
        response = self.client.get(reverse('signup_api'))

        expected_message = get_feedback_message('wrong_request', expected='POST', received='GET')
        self.assertContains(response, expected_message, status_code=405)
