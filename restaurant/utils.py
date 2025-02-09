import re
from django.core.exceptions import ValidationError


def phone_validator(phone: str) -> str:
    if not re.match(r"^09\d{9}$", phone):
        raise ValidationError("Phone number must contain only 11 digits and starts with 09")
    return phone


def seats_number_validator(seats_number: int) -> int:
    if seats_number < 4 or seats_number > 10:
        raise ValidationError("Seats number must br between 4 and 10")
    return seats_number