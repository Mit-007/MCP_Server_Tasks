import time

import pytest

from src.tasks_mcp_server.task_2.auth.token_auth import (
    check_token_expiry,
    create_token,
    extract_bearer_token,
    get_token,
    verify_token,
)
from src.tasks_mcp_server.task_2.data.token import TOKEN_REGISTRY


@pytest.fixture(autouse=True)
def reset_token_registry():
    """Reset token registry before and after each test."""
    TOKEN_REGISTRY.clear()

    yield

    TOKEN_REGISTRY.clear()


class TestTokenAuth:
    """Test token authentication functions."""

    # --> create_token
   
    @pytest.mark.parametrize(
        "scopes",
        [
            ["read", "write"],
            ["read"],
            [],
        ],
        ids=[
            "multiple_scopes",
            "single_scope",
            "empty_scopes",
        ],
    )
    def test_create_token_valid(self, scopes):
        """Test creating tokens with valid scope lists."""

        token = create_token(scopes)

        assert isinstance(token, str)
        assert len(token) > 0
        assert token in TOKEN_REGISTRY
        assert TOKEN_REGISTRY[token]["scopes"] == scopes

    @pytest.mark.parametrize(
        "scopes",
        [
            "read",
            ["read", 123],
        ],
        ids=[
            "scopes_not_list",
            "scope_not_string",
        ],
    )
    def test_create_token_invalid(self, scopes):
        """Test creating tokens with invalid scopes."""

        with pytest.raises(ValueError):
            create_token(scopes)

    def test_create_token_unique_tokens(self):
        """Test that creating tokens generates unique token values."""

        token1 = create_token(["read"])
        token2 = create_token(["write"])

        assert token1 in TOKEN_REGISTRY
        assert token2 in TOKEN_REGISTRY
        assert token1 != token2

    # --> get_token

    @pytest.mark.parametrize(
        "token_input, expected",
        [
            ("invalid_token_xyz", None),
            ("", None),
            ("   ", None),
            (123, None),
        ],
        ids=[
            "nonexistent_token",
            "empty_token",
            "whitespace_token",
            "invalid_token_type",
        ],
    )
    def test_get_token_invalid(self, token_input, expected):
        """Test retrieving invalid tokens."""

        result = get_token(token_input)

        assert result is expected

    def test_get_token_valid(self):
        """Test retrieving a valid token."""

        token = create_token(["read", "write"])

        result = get_token(token)

        assert result is not None
        assert result["scopes"] == ["read", "write"]



    # --> extract_bearer_token

    @pytest.mark.parametrize(
        "auth_header, expected_token",
        [
            ("Bearer test_token_123", "test_token_123"),
            ("bearer test_token_123", "test_token_123"),
        ],
        ids=[
            "uppercase_bearer",
            "lowercase_bearer",
        ],
    )
    def test_extract_bearer_token_valid(
        self,
        auth_header,
        expected_token,
    ):
        """Test extracting valid Bearer tokens."""

        token = extract_bearer_token(auth_header)

        assert token == expected_token

    @pytest.mark.parametrize(
        "auth_header",
        [
            None,
            "",
            "Basic test_token_123",
            "Bearer ",
            "Bearer token extra",
            123,
        ],
        ids=[
            "none_header",
            "empty_header",
            "wrong_scheme",
            "missing_token",
            "invalid_format",
            "invalid_header_type",
        ],
    )
    def test_extract_bearer_token_invalid(self, auth_header):
        """Test extracting tokens from invalid authorization headers."""

        token = extract_bearer_token(auth_header)

        assert token is None



    # --> verify_token

    def test_verify_token_valid(self):
        """Test verifying a valid token."""

        token = create_token(["read", "write"])
        auth_header = f"Bearer {token}"

        token_info, error = verify_token(auth_header)

        assert token_info is not None
        assert error is None
        assert token_info["scopes"] == ["read", "write"]

    @pytest.mark.parametrize(
        "auth_header",
        [
            "Bearer invalid_token_xyz",
            None,
            "InvalidFormat",
        ],
        ids=[
            "invalid_token",
            "none_header",
            "malformed_header",
        ],
    )
    def test_verify_token_invalid(self, auth_header):
        """Test verifying invalid authorization headers or tokens."""

        token_info, error = verify_token(auth_header)

        assert token_info is None
        assert error is not None

    # --> check_token_expiry

    @pytest.mark.parametrize(
        "token_info",
        [
            None,
            "not_a_dict",
        ],
        ids=[
            "none_token_info",
            "invalid_token_info_type",
        ],
    )
    def test_check_token_expiry_invalid(self, token_info):
        """Test expiry check with invalid token information."""

        is_valid, expired_seconds = check_token_expiry(token_info)

        assert is_valid is False
        assert expired_seconds == 0

    def test_check_token_expiry_no_expiration(self):
        """Test token without expiration."""

        token = create_token(["read"])
        token_info = get_token(token)

        is_valid, expired_seconds = check_token_expiry(token_info)

        assert is_valid is True
        assert expired_seconds == 0

    def test_check_token_expiry_not_expired(self):
        """Test token that has not expired."""

        token_info = {
            "scopes": ["read"],
            "expires_at": int(time.time()) + 3600,
        }

        is_valid, expired_seconds = check_token_expiry(token_info)

        assert is_valid is True
        assert expired_seconds == 0

    def test_check_token_expiry_expired(self):
        """Test expired token."""

        token_info = {
            "scopes": ["read"],
            "expires_at": int(time.time()) - 3600,
        }

        is_valid, expired_seconds = check_token_expiry(token_info)

        assert is_valid is False
        assert expired_seconds > 0