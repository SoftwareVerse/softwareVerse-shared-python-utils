import phonenumbers
from typing import Optional

PHONE_NUMBER_JSON_SCHEMA_EXTRA = {
    "example": "+27821234567",
    "pattern": r"^\+[1-9]\d{1,14}$",
    "description": "Phone number in E.164 format.",
}


def validate_phone_number_format(phone: Optional[str]) -> Optional[str]:
    """Validate and format the phone number to E.164 standard."""
    if not phone:
        return phone

    try:
        parsed = phonenumbers.parse(phone, None)  # No default region
        if not phonenumbers.is_valid_number(parsed):
            raise ValueError("Invalid phone number.")
    except phonenumbers.NumberParseException as exc:
        raise ValueError("Invalid phone number format.") from exc

    return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
