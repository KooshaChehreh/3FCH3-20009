import jwt
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from users.models import User


def generate_access_token(user: User) -> str:
    time_now = timezone.now()
    base_payload = {
        "exp": time_now + timedelta(seconds=settings.JWT_EXPIRATION_SECS),  # Expiration at (seconds)
        "iat": time_now,  # Issued at (seconds)
        "id": user.id,
        "phone": user.phone,
    }

    return jwt.encode(
        payload=base_payload,
        key=settings.JWT_SECRET_KEY,
        algorithm="HS256",
    )


