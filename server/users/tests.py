from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User


class AuthenticationAPITestCase(APITestCase):
    def setUp(self):
        """Set up test data before each test"""
        self.user = User.objects.create_user(
            username='testkeeper',
            email='test@zoo.com',
            password='testpass123'
        )

    def test_register_user(self):
        """Test user registration with JWT"""
        url = '/api/auth/register/'
        data = {
            'username': 'newkeeper',
            'email': 'newkeeper@zoo.com',
            'password': 'newpass123'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], 'newkeeper')

        # Verify user was created
        self.assertTrue(
            User.objects.filter(username='newkeeper').exists()
        )

    def test_register_duplicate_username(self):
        """Test that duplicate usernames are rejected"""
        url = '/api/auth/register/'
        data = {
            'username': 'testkeeper',  # Already exists
            'email': 'another@zoo.com',
            'password': 'pass123'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_login_valid_credentials(self):
        """Test login with valid credentials returns JWT tokens"""
        url = '/api/auth/login/'
        data = {
            'username': 'testkeeper',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], 'testkeeper')

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        url = '/api/auth/login/'
        data = {
            'username': 'testkeeper',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
        self.assertIn('error', response.data)

    def test_login_missing_credentials(self):
        """Test login with missing credentials"""
        url = '/api/auth/login/'
        data = {'username': 'testkeeper'}  # Missing password
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_token(self):
        """Test refreshing access token with refresh token"""
        # First login to get tokens
        login_url = '/api/auth/login/'
        login_data = {
            'username': 'testkeeper',
            'password': 'testpass123'
        }
        login_response = self.client.post(
            login_url,
            login_data,
            format='json'
        )
        refresh_token = login_response.data['refresh']

        # Now refresh the token
        refresh_url = '/api/auth/refresh/'
        refresh_data = {'refresh': refresh_token}
        response = self.client.post(
            refresh_url,
            refresh_data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_refresh_token_invalid(self):
        """Test refresh with invalid token"""
        url = '/api/auth/refresh/'
        data = {'refresh': 'invalid_token_here'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_authenticated_request(self):
        """Test making authenticated request with JWT"""
        # Login to get access token
        login_url = '/api/auth/login/'
        login_data = {
            'username': 'testkeeper',
            'password': 'testpass123'
        }
        login_response = self.client.post(
            login_url,
            login_data,
            format='json'
        )
        access_token = login_response.data['access']

        # Make authenticated request
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )
        response = self.client.get('/api/auth/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertEqual(
            response.data['user']['username'],
            'testkeeper'
        )

    def test_logout(self):
        """Test logout endpoint"""
        url = '/api/auth/logout/'
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
