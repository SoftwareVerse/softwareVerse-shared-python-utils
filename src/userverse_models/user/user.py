from typing import Optional, Literal
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator, Field

from sverse_generic_models.generic_pagination import PaginationParams
from sverse_validators.phone_number import (
    PHONE_NUMBER_JSON_SCHEMA_EXTRA,
    validate_phone_number_format,
)


class UserLoginModel(BaseModel):
    """Model for user login."""

    email: EmailStr
    password: str


class UserUpdateModel(BaseModel):
    """Model for updating user details."""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = Field(
        None, json_schema_extra=PHONE_NUMBER_JSON_SCHEMA_EXTRA
    )
    password: Optional[str] = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone number format."""
        return validate_phone_number_format(v)


class UserCreateModel(BaseModel):
    """Model for creating a new user."""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = Field(
        None, json_schema_extra=PHONE_NUMBER_JSON_SCHEMA_EXTRA
    )

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone number format."""
        return validate_phone_number_format(v)


class UserReadModel(BaseModel):
    """Model representing a user."""

    id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: EmailStr
    phone_number: Optional[str] = Field(
        None, json_schema_extra=PHONE_NUMBER_JSON_SCHEMA_EXTRA
    )
    status: Optional[str] = None  # <-- Add this
    is_superuser: bool = Field(
        False, description="Indicates if the user has superuser privileges"
    )


class TokenResponseModel(BaseModel):
    """Model for token response."""

    token_type: Literal["bearer"] = Field(
        "bearer",
        description="Type of the token",
    )
    access_token: str = Field(..., description="JWT access token")
    access_token_expiration: str = Field(
        ..., description="Access token expiration time in 'YYYY-MM-DD HH:MM:SS' format"
    )
    refresh_token: str = Field(..., description="JWT refresh token")
    refresh_token_expiration: str = Field(
        ..., description="Refresh token expiration time in 'YYYY-MM-DD HH:MM:SS' format"
    )


class RefreshTokenRequestModel(BaseModel):
    """Model for refresh token requests."""

    refresh_token: str = Field(..., description="JWT refresh token")


class TokenRevocationResponseModel(BaseModel):
    """Model for refresh token revocation responses."""

    revoked: bool = Field(
        True,
        description="Indicates whether the presented refresh token family was revoked",
    )


class UserQueryParams(PaginationParams):
    """Model for querying users with optional filters."""

    role_name: Optional[str] = Field(None, description="Filter by role name")
    first_name: Optional[str] = Field(None, description="Filter by user first name")
    last_name: Optional[str] = Field(None, description="Filter by user last name")
    email: Optional[str] = Field(None, description="Filter by user email")
