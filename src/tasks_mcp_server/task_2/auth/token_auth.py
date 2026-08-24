import time
import secrets
import string
from src.tasks_mcp_server.task_2.data.token import TOKEN_REGISTRY
from src.tasks_mcp_server.task_2.core.constant import Available_scope, length_of_token
from src.tasks_mcp_server.task_2.core.logger import logger


def create_token(scopes: list[Available_scope]) -> str:
    """
    Create a new authentication token with specified scopes.
    
    Args:
        scopes: List of scopes to assign to the token
        
    Returns:
        A randomly generated token string
        
    Raises:
        ValueError: If scopes is invalid
    """
    try:
        if not isinstance(scopes, list):
            logger.error(f"Invalid scopes type: expected list, got {type(scopes)}")
            raise ValueError("Scopes must be a list")
            
        if not scopes:
            logger.warning("Creating token with empty scopes list")
        
        for scope in scopes:
            if not isinstance(scope, str):
                logger.error(f"Invalid scope type in list: {type(scope)}")
                raise ValueError(f"Each scope must be a string, got {type(scope)}")
        
        alphabet = string.ascii_letters + string.digits
        
        if not isinstance(length_of_token, int) or length_of_token <= 0:
            logger.error(f"Invalid length_of_token: {length_of_token}")
            raise ValueError("Token length must be a positive integer")
        
        token = "".join(
            secrets.choice(alphabet)
            for _ in range(length_of_token)
        )
 
        if token in TOKEN_REGISTRY:
            logger.warning(f"Generated duplicate token (collision), regenerating...")
            return create_token(scopes)
 
        TOKEN_REGISTRY[token] = {
            "scopes": scopes,
        }
        
        logger.info(f"Token created successfully with scopes: {scopes}")
 
        return token
        
    except ValueError as ve:
        raise ve
    except Exception as e:
        logger.error(f"Unexpected error creating token: {str(e)}")
        raise Exception(f"Failed to create token: {str(e)}")


def get_token(token: str) -> dict | None:
    """
    Retrieve token information from the registry.
    
    Args:
        token: The token string to look up
        
    Returns:
        Token information dictionary if found, None otherwise
    """
    try:
        if not isinstance(token, str):
            logger.debug(f"Invalid token type: expected str, got {type(token)}")
            return None
            
        if not token or not token.strip():
            logger.debug("Empty token provided")
            return None
        
        token = token.strip()
        result = TOKEN_REGISTRY.get(token)
        
        if result is None:
            logger.debug(f"Token not found in registry")
        
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error retrieving token: {str(e)}")
        return None


def extract_bearer_token(
    authorization: str | None,
) -> str | None:
    """
    Extract a bearer token from an Authorization value.
    
    Args:
        authorization: The Authorization header value
        
    Returns:
        The extracted token string if valid, None otherwise
    """
    try:
        if authorization is None:
            logger.debug("Authorization header is None")
            return None
 
        if not isinstance(authorization, str):
            logger.debug(f"Invalid authorization type: expected str, got {type(authorization)}")
            return None
 
        authorization = authorization.strip()
        
        if not authorization:
            logger.debug("Authorization header is empty")
            return None
        
        parts = authorization.split(" ")
        
        if len(parts) != 2:
            logger.debug(f"Invalid authorization header format: expected 2 parts, got {len(parts)}")
            return None
 
        scheme, token = parts
 
        if scheme.lower() != "bearer":
            logger.debug(f"Invalid scheme: expected 'Bearer', got '{scheme}'")
            return None
 
        token = token.strip()
 
        if not token:
            logger.debug("Bearer token is empty")
            return None
 
        logger.debug("Bearer token extracted successfully")
        return token
        
    except ValueError as ve:
        logger.debug(f"Error parsing authorization header: {str(ve)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error extracting bearer token: {str(e)}")
        return None



def verify_token(authorization: str | None,) -> tuple[dict | None, str | None]:
    """
    Verify token authentication.
 
    Args:
        authorization: The Authorization header value
        
    Returns:
        (token_info, None) when valid.
        (None, error_message) when invalid or expired.
    """
    try:
        if authorization is None:
            logger.warning("Authorization header is None")
            return None, "Missing or invalid Authorization header"
 
        token = extract_bearer_token(authorization)
        
        if token is None:
            logger.warning("Failed to extract bearer token from authorization header")
            return None, "Missing or invalid Authorization header"
 
        token_info = TOKEN_REGISTRY.get(token)
 
        if token_info is None:
            logger.warning(f"Token not found in registry")
            return None, "Invalid authentication token"
 
        if not isinstance(token_info, dict):
            logger.error(f"Invalid token_info structure: expected dict, got {type(token_info)}")
            return None, "Token data is corrupted"
 
        logger.info("Token verification successful")
        return token_info, None
 
    except Exception as e:
        logger.error(f"Unexpected error verifying token: {str(e)}")
        return None, "Token verification failed"



def check_token_expiry(
    token_info: dict,
) -> tuple[bool, int]:
    """
    Check whether a token has expired.
 
    Args:
        token_info: Dictionary containing token information
        
    Returns:
        (True, 0) if the token is still valid.
        (False, seconds_expired) if the token has expired.
    """
    try:
        if not isinstance(token_info, dict):
            logger.error(f"Invalid token_info type: expected dict, got {type(token_info)}")
            return False, 0
 
        expires_at = token_info.get("expires_at")
 
        if expires_at is None:
            logger.warning("Token has no expiration time configured")
            return False, 0
 
        if not isinstance(expires_at, (int, float)):
            logger.error(f"Invalid expires_at type: expected int or float, got {type(expires_at)}")
            return False, 0
 
        if expires_at < 0:
            logger.error(f"Invalid expires_at value: {expires_at} (negative timestamp)")
            return False, 0
 
        try:
            current_time = int(time.time())
        except Exception as e:
            logger.error(f"Failed to get current time: {str(e)}")
            return False, 0
 
        if current_time < expires_at:
            logger.debug("Token is still valid")
            return True, 0
 
        seconds_expired = current_time - expires_at
 
        logger.warning(f"Token has expired {seconds_expired} seconds ago")
        return False, seconds_expired
        
    except Exception as e:
        logger.error(f"Unexpected error checking token expiry: {str(e)}")
        return False, 0