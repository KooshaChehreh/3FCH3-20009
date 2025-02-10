from model_bakery import baker
from users.models import User
from test_utils import make_authenticated_api_client
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.hashers import make_password
from exceptions import *
from rest_framework import status
from django.utils import timezone




class UsersTest(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.user = baker.make(User, username="parstasmim", password=make_password("pars123"))

        # Authenticated and non-authenticated API clients
        self.user_authenticated_client = make_authenticated_api_client(user=self.user)
        self.not_authenticated_client = APIClient()

        # Endpoints
        self.create_user_url = "/users/sign-up/"
        self.login_url = "/users/login/verify-password/"

    def test_create_user_success(self):
        data = {
            "username": "new_user",
            "password": "new_password123"
        }
        response = self.not_authenticated_client.post(self.create_user_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], data["username"])
        self.assertTrue(User.objects.filter(username=data["username"]).exists())

    def test_create_user_username_already_exists(self):
        data = {
            "username": "parstasmim",
            "password": "another_password"
        }
        response = self.not_authenticated_client.post(self.create_user_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], UsernameAlreadyExists.default_code)

    def test_login_successful(self):
        login_data = {
            "username": "parstasmim",
            "password": "pars123"
        }
        response = self.not_authenticated_client.post(self.login_url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)

    def test_login_invalid_credentials(self):
        invalid_login_data = {
            "username": "parstasmim",
            "password": "wrongpassword"
        }
        response = self.not_authenticated_client.post(self.login_url, invalid_login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], InvalidUsernameOrPassword.default_code)

    def test_login_account_suspended(self):
        self.user.suspended_at = timezone.now()
        self.user.save()
        suspended_login_data = {
            "username": "parstasmim",
            "password": "pars123"
        }
        response = self.not_authenticated_client.post(self.login_url, suspended_login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["code"], AccountSuspended.default_code)
