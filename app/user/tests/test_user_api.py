from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test user api (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_succes(self):
        """Test create user with valid payload is successful"""
        payload = {
            'email': 'test@test.com',
            'password': 'passwordTest',
            'name': 'NameTest_user'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_creat_user_exist(self):
        """Test create if exist"""
        payload = {'email': 'test@test.com', 'password': 'passwordTest'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 5 characters"""
        payload = {'email': 'test@ts.com.temp', 'password': 'pass'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_token_for_user(self):
        """User get token creat user"""
        payload = {'email': 'correct@email.com', 'password': 'correct_pasword123'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_token_if_invalid_credentials(self):
        create_user(email = 'test@emaail.com', password = 'testpass')
        payload = {'email': 'email@email.com', 'password': 'xddsas'}

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_token_if_missing_fields(self):
        """Test get token if user miss fill one fields"""
        create_user(email='test@test.com', password='passssword')
        payload = { 'email': '', 'password': 'pass123'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)
