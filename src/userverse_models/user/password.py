from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class PasswordResetMethod(str, Enum):
    """Available password reset delivery methods."""

    OTP = "otp"
    MAGIC_LINK = "magic_link"


class PasswordResetRequest(BaseModel):
    """Model for requesting a password reset via email."""

    email: EmailStr
    method: PasswordResetMethod = PasswordResetMethod.OTP


class OTPValidationRequest(BaseModel):
    """Model for validating OTP during password reset."""

    otp: str


class MagicLinkPasswordResetConfirmRequest(BaseModel):
    """Model for completing password reset via magic link token."""

    token: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=1)
