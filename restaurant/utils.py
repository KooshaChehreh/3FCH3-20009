import re
from django.core.exceptions import ValidationError


def phone_validator(phone: str) -> str:
    if not re.match(r"^09\d{9}$", phone):
        raise ValidationError("Phone number must contain only 11 digits and starts with 09")
    return phone