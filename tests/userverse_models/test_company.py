import pytest
from pydantic import ValidationError

from userverse_models.company.address import CompanyAddressModel
from userverse_models.company.company import (
    CompanyCreateModel,
    CompanyQueryParamsModel,
    CompanyReadModel,
    CompanyUpdateModel,
)
from userverse_models.company.user import CompanyUserAddModel, CompanyUserReadModel


class TestCompanyAddressModel:
    """Tests for company address model."""

    def test_optional_fields_default_to_none(self):
        """Address fields should default to None when not provided."""
        address = CompanyAddressModel()
        assert address.street is None
        assert address.city is None
        assert address.state is None
        assert address.postal_code is None
        assert address.country is None

    def test_address_accepts_values(self):
        """Address fields should accept provided values."""
        address = CompanyAddressModel(
            street="123 Main St",
            city="Cape Town",
            state="CT",
            postal_code="8000",
            country="South Africa",
        )
        assert address.street == "123 Main St"
        assert address.city == "Cape Town"
        assert address.state == "CT"
        assert address.postal_code == "8000"
        assert address.country == "South Africa"


class TestCompanyModels:
    """Tests for company models."""

    def test_company_create_formats_phone_number(self):
        """Phone number should be formatted to E.164."""
        company = CompanyCreateModel(
            phone_number="+12025550123", email="info@example.com"
        )
        assert company.phone_number == "+12025550123"

    def test_company_update_rejects_invalid_phone(self):
        """Invalid phone numbers should raise ValidationError."""
        with pytest.raises(ValidationError):
            CompanyUpdateModel(phone_number="123")

    def test_company_read_requires_id_and_email(self):
        """CompanyReadModel should require id and email."""
        with pytest.raises(ValidationError):
            CompanyReadModel()

    def test_company_query_params_defaults(self):
        """Query params should inherit pagination defaults."""
        params = CompanyQueryParamsModel(page=3)
        assert params.limit == 10
        assert params.offset() == 20


class TestCompanyUserModels:
    """Tests for company user models."""

    def test_company_user_add_defaults_role(self):
        """Role should default to Viewer when not provided."""
        user = CompanyUserAddModel(email="user@example.com")
        assert user.role == "Viewer"

    def test_company_user_read_requires_role(self):
        """CompanyUserReadModel should require role_name."""
        with pytest.raises(ValidationError):
            CompanyUserReadModel(
                id="550e8400-e29b-41d4-a716-446655440000",
                email="user@example.com",
            )
