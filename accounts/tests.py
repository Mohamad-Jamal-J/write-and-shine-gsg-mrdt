from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class AccountTests(TestCase):
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
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Account created successfully.')

    def test_login_success(self):
        """Test successful login."""
        self.User.objects.create_user(**self.user_data)
        response = self.client.post(reverse('login_api'), {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login successful.')

    def test_login_wrong_password(self):
        """Test login with wrong password."""
        self.User.objects.create_user(**self.user_data)
        response = self.client.post(reverse('login_api'), {
            'email': self.user_data['email'],
            'password': 'WrongPassword!'
        })
        self.assertEqual(response.status_code, 400)

    def test_logout_success(self):
        """Test successful logout."""
        self.User.objects.create_user(**self.user_data)
        self.client.login(email=self.user_data['email'], password=self.user_data['password'])
        response = self.client.post(reverse('logout_api'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Logout successful.')

    def test_logout_not_logged_in(self):
        """Test logout when not logged in."""
        response = self.client.post(reverse('logout_api'))
        self.assertEqual(response.status_code, 400)
