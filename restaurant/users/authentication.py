from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User

class IsAuthenticatedWithToken(BaseAuthentication):
    keyword = "JWT"

    def authenticate_header(self, request):
        return 'Bearer realm="api"'
    
    def authenticate(self, request):
        try:
            user = User.from_request(request, anonymous_raise_401=True)
            if user is None:
                return None
            return (user, None)
        except AuthenticationFailed as e:
            raise AuthenticationFailed(
                detail={"message": "Authentication failed", "code": "authentication_failed"}
            )