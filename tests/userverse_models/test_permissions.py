import pytest
from pydantic import ValidationError

from userverse_models.permissions import (
    PermissionCreateModel,
    PermissionQueryParamsModel,
    PermissionReadModel,
    PermissionScope,
    PermissionUpdateModel,
)


class TestPermissionCreateModel:
    def test_trims_permission_name(self):
        permission = PermissionCreateModel(name="  company.read  ")
        assert permission.name == "company.read"

    @pytest.mark.parametrize("name", ["", "   "])
    def test_rejects_blank_permission_name(self, name):
        with pytest.raises(ValidationError):
            PermissionCreateModel(name=name)


class TestPermissionUpdateModel:
    def test_requires_at_least_one_field(self):
        with pytest.raises(ValidationError):
            PermissionUpdateModel()

    def test_rejects_null_name(self):
        with pytest.raises(ValidationError):
            PermissionUpdateModel(name=None)

    def test_allows_explicit_null_description(self):
        permission = PermissionUpdateModel(description=None)
        assert permission.description is None

    def test_trims_updated_name(self):
        permission = PermissionUpdateModel(name="  company.update  ")
        assert permission.name == "company.update"


class TestPermissionReadModel:
    def test_accepts_global_permission(self):
        permission = PermissionReadModel(
            id="550e8400-e29b-41d4-a716-446655440000",
            name="company.read",
            scope="global",
        )

        assert permission.scope is PermissionScope.GLOBAL
        assert permission.company_id is None

    def test_accepts_company_permission(self):
        permission = PermissionReadModel(
            id="550e8400-e29b-41d4-a716-446655440000",
            name="invoice.approve",
            scope="company",
            company_id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert permission.scope is PermissionScope.COMPANY
        assert str(permission.company_id) == "123e4567-e89b-12d3-a456-426614174000"


class TestPermissionQueryParamsModel:
    def test_inherits_pagination_and_filters(self):
        params = PermissionQueryParamsModel(
            page=2,
            limit=25,
            name="company",
            description="read",
        )

        assert params.offset() == 25
        assert params.name == "company"
        assert params.description == "read"
