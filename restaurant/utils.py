import re
from django.core.exceptions import ValidationError
from django.conf import settings

def phone_validator(phone: str) -> str:
    if not re.match(r"^09\d{9}$", phone):
        raise ValidationError("Phone number must contain only 11 digits and starts with 09")
    return phone


def seats_number_validator(seats_number: int) -> int:
    if seats_number < settings.TABLE_MIN_SEATS or seats_number > settings.TABLE_MAX_SEATS:
        raise ValidationError(f"Seats number must br between {settings.TABLE_MIN_SEATS} and {settings.TABLE_MAX_SEATS}")
    return seats_number