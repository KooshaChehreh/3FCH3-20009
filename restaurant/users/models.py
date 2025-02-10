from django.db import models
import jwt
from django.db import models
from django.conf import settings
from utils import phone_validator
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.exceptions import AuthenticationFailed


class User(models.Model):
    username = models.CharField(
        max_length=64,
        verbose_name="نام کاربری",
    )
    phone = models.CharField(
        blank=True,
        null=True,
        max_length=11,
        validators=[phone_validator],
        verbose_name="تلفن همراه",
    )

    password = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name="پسورد",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="ایجاد شده در"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="بروز شده در")
    suspended_at = models.DateTimeField(
        blank=True, null=True, verbose_name="تاریخ تعلیق"
    )

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"
        ordering = ["-id"]

    @staticmethod
    def hash_password(raw_password):
        return make_password(password=raw_password)

    def check_password(self, entered_password):
        if bool(self.password):
            return check_password(password=entered_password, encoded=self.password)
        else:
            return False
    
    @staticmethod
    def from_request(request, anonymous_raise_401=False):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            if anonymous_raise_401:
                raise AuthenticationFailed
            else:
                return None
        try:
            access_token = auth_header.split(" ")[1]
            payload = jwt.decode(
                jwt=access_token,
                key=settings.JWT_SECRET_KEY,
                algorithms=["HS256"],
            )
            print(payload)
        except (jwt.exceptions.DecodeError, jwt.exceptions.DecodeError):
            raise AuthenticationFailed(
                detail={"message": "Invalid token", "code": "invalid_token"}
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(
                detail={"message": "Expired token", "code": "token_expired"}
            )
        user_id = payload.get("id", None)
        if not user_id:
            return None
        try:
            user = User.objects.get(id=user_id)
            return user
        except User.DoesNotExist:
            return None
        
    def is_suspended(self):
        return self.suspended_at is not None
    
