from pydantic import BaseModel, EmailStr, Field

from .roles import CompanyDefaultRoles
from ..user.user import UserReadModel


class CompanyUserReadModel(UserReadModel):
    """Model representing a user within a company, including their role."""

    role_name: str


class CompanyUserAddModel(BaseModel):
    """Model for adding a user to a company with a specific role."""

    email: EmailStr = Field(
        ...,
        json_schema_extra={"example": "user.one@email.com"},
    )
    role: str = Field(
        default=CompanyDefaultRoles.VIEWER.name_value,
        json_schema_extra={"example": "Viewer"},
    )


class CompanyUserRoleUpdateModel(BaseModel):
    """Model for updating a company user's role."""

    role: str = Field(
        ...,
        json_schema_extra={"example": "Administrator"},
    )
