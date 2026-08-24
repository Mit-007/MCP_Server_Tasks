import time
import secrets
import string
from src.tasks_mcp_server.task_3.call_log_server.data.token import TOKEN_REGISTRY
from src.tasks_mcp_server.task_3.call_log_server.core.constant import Available_scope , length_of_token


def create_token(scopes: list[Available_scope]) -> str:

    alphabet = string.ascii_letters + string.digits
    token = "".join(
        secrets.choice(alphabet)
        for _ in range(length_of_token)
    )

    TOKEN_REGISTRY[token] = {
        "scopes": scopes,
    }

    return token


def get_token(token: str) -> dict | None:
    return TOKEN_REGISTRY.get(token)

def extract_bearer_token(
    authorization: str | None,
) -> str | None:
    """Extract a bearer token from an Authorization value."""

    if not authorization:
        return None

    authorization = authorization.strip()
    
    parts = authorization.split(" ")
    
    if len(parts) != 2:
        return None

    scheme, token = parts

    if scheme.lower() != "bearer":
        return None

    token = token.strip()

    if not token:
        return None

    return token

def verify_token(authorization: str | None,) -> tuple[dict | None, str | None]:
    """
    Verify token authentication and expiry.

    Returns:
        (token_info, None) when valid.

        (None, error_message) when invalid or expired.
    """

    token = extract_bearer_token(authorization)
    
    if token is None:
        return None, "Missing or invalid Authorization header"

    token_info = TOKEN_REGISTRY.get(token)

    if token_info is None:
        return None, "Invalid authentication token"

    # expires_at = token_info.get("expires_at")

    # if expires_at is None:
    #     return None, "Token expiration is not configured"

    # now = int(time.time())

    # if now >= expires_at:
    #     expired_seconds = now - expires_at

    #     return (
    #         None,
    #         f"Token expired {expired_seconds} seconds ago",
    #     )

    return token_info, None



def check_token_expiry(
    token_info: dict,
) -> tuple[bool, int]:
    """
    Check whether a token has expired.

    Returns:
        (True, 0) if the token is still valid.

        (False, seconds_expired) if the token has expired.
    """

    expires_at = token_info.get("expires_at")

    if expires_at is None:
        # Treat missing expiry as invalid configuration.
        return False, 0

    current_time = int(time.time())

    if current_time < expires_at:
        return True, 0

    seconds_expired = current_time - expires_at

    return False, seconds_expired