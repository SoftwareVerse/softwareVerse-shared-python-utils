from enum import Enum
from typing import Optional
from pydantic import BaseModel
from pydantic import field_validator, Field

from sverse_generic_models.generic_pagination import PaginationParams
from userverse_models.permissions import PermissionReadModel


class CompanyDefaultRoles(str, Enum):
    """Enumeration of default company roles with descriptions."""

    OWNER = "Owner: Full access to manage users and data"
    ADMINISTRATOR = "Administrator: Full access to manage users and data"
    VIEWER = "Viewer: Read-only access to company data"

    @property
    def name_value(self) -> str:
        """Returns just the role name (e.g., 'Administrator')."""
        return self.value.split(":")[0].strip()

    @property
    def description(self) -> str:
        """Returns just the role description."""
        return self.value.split(":", 1)[1].strip()


class RoleCreateModel(BaseModel):
    """Model for creating a new role."""

    name: str
    description: Optional[str]


class RoleUpdateModel(BaseModel):
    """Model for updating a role."""

    name: Optional[str]
    description: Optional[str]


class RoleDeleteModel(BaseModel):
    """Model for deleting a role with replacement."""

    replacement_role_name: str
    role_name_to_delete: str

    @field_validator("role_name_to_delete")
    @classmethod
    def validate_not_default_role(cls, v: str) -> str:
        """Ensure that default system roles cannot be deleted."""
        default_roles = {r.name_value for r in CompanyDefaultRoles}
        if v in default_roles:
            raise ValueError(f"Cannot delete default system role: '{v}'")
        return v


class RoleReadModel(BaseModel):
    """Model representing a role."""

    id: str | None = None
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: list[PermissionReadModel] = Field(default_factory=list)


class RoleAssignCompaniesModel(BaseModel):
    """Model for assigning a role to multiple companies."""

    company_ids: list[str]


class RoleQueryParamsModel(PaginationParams):
    """Model for querying roles with optional filters."""

    name: Optional[str] = Field(None, description="Filter by role name")
    description: Optional[str] = Field(None, description="Filter by role description")
