import pytest
from pydantic import ValidationError

from userverse_models.user.password import OTPValidationRequest, PasswordResetRequest
from userverse_models.user.user import (
    RefreshTokenRequestModel,
    TokenResponseModel,
    TokenRevocationResponseModel,
    UserCreateModel,
    UserLoginModel,
    UserQueryParams,
    UserReadModel,
    UserUpdateModel,
)


class TestUserLoginModel:
    """Tests for user login model."""

    def test_login_requires_valid_email(self):
        """Invalid email should raise a ValidationError."""
        with pytest.raises(ValidationError):
            UserLoginModel(email="not-an-email", password="secret")


class TestUserCreateModel:
    """Tests for user creation model."""

    def test_user_create_formats_phone_number(self):
        """Phone numbers should be formatted to E.164."""
        user = UserCreateModel(phone_number="+12025550123")
        assert user.phone_number == "+12025550123"


class TestUserUpdateModel:
    """Tests for user update model."""

    def test_user_update_rejects_invalid_phone(self):
        """Invalid phone numbers should raise ValidationError."""
        with pytest.raises(ValidationError):
            UserUpdateModel(phone_number="123")


class TestUserReadModel:
    """Tests for user read model."""

    def test_defaults_for_optional_fields(self):
        """Optional fields should default to None or False as configured."""
        user = UserReadModel(
            id="550e8400-e29b-41d4-a716-446655440000", email="user@example.com"
        )
        assert user.status is None
        assert user.is_superuser is False


class TestTokenResponseModel:
    """Tests for token response model."""

    def test_default_token_type(self):
        """Token type should default to bearer."""
        token = TokenResponseModel(
            access_token="access",
            access_token_expiration="2025-01-01 00:00:00",
            refresh_token="refresh",
            refresh_token_expiration="2025-01-02 00:00:00",
        )
        assert token.token_type == "bearer"


class TestUserQueryParams:
    """Tests for user query params."""

    def test_inherits_pagination_defaults(self):
        """Pagination defaults should be applied."""
        params = UserQueryParams(page=2)
        assert params.limit == 10
        assert params.offset() == 10


class TestPasswordModels:
    """Tests for password reset models."""

    def test_password_reset_requires_valid_email(self):
        """Invalid emails should raise ValidationError."""
        with pytest.raises(ValidationError):
            PasswordResetRequest(email="bad-email")

    def test_password_reset_defaults_to_otp(self):
        """Password reset requests should default to the OTP flow."""
        request = PasswordResetRequest(email="user@example.com")
        assert request.method == "otp"

    def test_otp_validation_accepts_value(self):
        """OTP should be preserved as provided."""
        request = OTPValidationRequest(otp="123456")
        assert request.otp == "123456"


class TestTokenModels:
    """Tests for refresh/revocation token models."""

    def test_refresh_token_request_preserves_value(self):
        request = RefreshTokenRequestModel(refresh_token="refresh-token")
        assert request.refresh_token == "refresh-token"

    def test_token_revocation_defaults_true(self):
        response = TokenRevocationResponseModel()
        assert response.revoked is True
