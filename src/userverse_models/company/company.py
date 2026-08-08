from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator, Field

from sverse_generic_models.generic_pagination import PaginationParams
from sverse_validators.phone_number import (
    PHONE_NUMBER_JSON_SCHEMA_EXTRA,
    validate_phone_number_format,
)

from .address import CompanyAddressModel
from .roles import RoleReadModel


class CompanyReadModel(BaseModel):
    """Model representing a company."""

    id: UUID
    name: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    phone_number: Optional[str] = Field(
        None, json_schema_extra=PHONE_NUMBER_JSON_SCHEMA_EXTRA
    )
    email: EmailStr
    address: Optional[CompanyAddressModel] = None


class UserCompanyReadModel(CompanyReadModel):
    """Model representing a company and the requesting user's role."""

    role: RoleReadModel


class CompanyUpdateModel(BaseModel):
    """Model for updating company details."""

    name: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    phone_number: Optional[str] = Field(
        None, json_schema_extra=PHONE_NUMBER_JSON_SCHEMA_EXTRA
    )
    address: Optional[CompanyAddressModel] = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone number format."""
        return validate_phone_number_format(v)


class CompanyCreateModel(BaseModel):
    """Model for creating a new company."""

    name: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    phone_number: Optional[str] = Field(
        None, json_schema_extra=PHONE_NUMBER_JSON_SCHEMA_EXTRA
    )
    email: EmailStr
    address: Optional[CompanyAddressModel] = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v: Optional[str]) -> Optional[str]:
        """Validate phone number format."""
        return validate_phone_number_format(v)


class CompanyQueryParamsModel(PaginationParams):
    """Model for querying companies with optional filters."""

    role_name: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    email: Optional[str] = None
