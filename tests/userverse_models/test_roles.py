import pytest
from pydantic import ValidationError

from userverse_models.company.roles import (
    CompanyDefaultRoles,
    RoleCreateModel,
    RoleDeleteModel,
    RoleQueryParamsModel,
    RoleReadModel,
    RoleUpdateModel,
)


class TestCompanyDefaultRoles:
    """Tests for default roles enum."""

    def test_name_and_description_properties(self):
        """Enum properties should split name and description."""
        assert CompanyDefaultRoles.OWNER.name_value == "Owner"
        assert CompanyDefaultRoles.ADMINISTRATOR.name_value == "Administrator"
        assert (
            CompanyDefaultRoles.ADMINISTRATOR.description
            == "Full access to manage users and data"
        )


class TestRoleModels:
    """Tests for role models."""

    def test_role_create_roundtrip(self):
        """RoleCreateModel should preserve provided values."""
        role = RoleCreateModel(name="Manager", description="Manages users")
        assert role.name == "Manager"
        assert role.description == "Manages users"

    def test_role_update_allows_partial(self):
        """RoleUpdateModel should allow optional fields."""
        role = RoleUpdateModel(name=None, description="Updated")
        assert role.name is None
        assert role.description == "Updated"

    def test_role_read_allows_optional_fields(self):
        """RoleReadModel should accept optional fields."""
        role = RoleReadModel(name=None, description=None)
        assert role.name is None
        assert role.description is None

    def test_role_delete_rejects_default_role(self):
        """Deleting a default role should raise ValidationError."""
        with pytest.raises(ValidationError):
            RoleDeleteModel(
                replacement_role_name="Manager",
                role_name_to_delete=CompanyDefaultRoles.ADMINISTRATOR.name_value,
            )

    def test_role_query_params_inherit_pagination(self):
        """Query params should inherit pagination defaults."""
        params = RoleQueryParamsModel(page=2, name="Admin")
        assert params.limit == 10
        assert params.offset() == 10
        assert params.name == "Admin"
