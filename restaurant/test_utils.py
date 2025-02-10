from rest_framework.test import APITestCase, APIClient
from users.models import User
from users.jwt_auth import generate_access_token



def make_authenticated_api_client(user: User) -> APIClient:
    api_client = APIClient()
    api_client.force_authenticate(user=user)
    return api_client


def make_authenticated_api_client_non_forced(user: User) -> APIClient:
    """
    Create an authenticated APIClient. Authentication is done by setting the auth header,
    ensuring that the target API authentication is not skipped and will be used during the test.
    """
    api_client = APIClient()
    auth_token = generate_access_token(user=user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + auth_token)
    return api_client