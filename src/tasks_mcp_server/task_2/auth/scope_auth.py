from src.tasks_mcp_server.task_2.core.logger import logger
from src.tasks_mcp_server.task_2.core.constant import VALID_SCOPES,READ_MCP_METHODS,READ_TOOLS,WRITE_TOOLS

def validate_scope(scope: str) -> bool:
    """
    Check whether a scope is supported by the authorization system.
    
    Args:
        scope: The scope string to validate
        
    Returns:
        True if scope is valid, False otherwise
    """
    try:
        if not isinstance(scope, str):
            logger.warning(f"Invalid scope type: expected str, got {type(scope)}")
            return False

        scope = scope.strip()
        
        if not scope:
            logger.warning("Scope cannot be empty or whitespace")
            return False
        
        result = scope in VALID_SCOPES
        
        if not result:
            logger.debug(f"Scope '{scope}' not in valid scopes: {VALID_SCOPES}")
            
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error validating scope '{scope}': {str(e)}")
        return False

    
def check_scope(
    token_info: dict,
    required_scope: str,
) -> bool:
    """
    Check whether the authenticated token has the required scope.
    
    Args:
        token_info: Dictionary containing token information including scopes
        required_scope: The scope required for the operation
        
    Returns:
        True if token has required scope, False otherwise
    """
    try:
        if not isinstance(token_info, dict):
            logger.error(f"Invalid token_info type: expected dict, got {type(token_info)}")
            return False
            
        if not isinstance(required_scope, str):
            logger.error(f"Invalid required_scope type: expected str, got {type(required_scope)}")
            return False
        
        if not validate_scope(required_scope):
            logger.warning(f"Required scope '{required_scope}' is not valid")
            return False
 
        scopes = token_info.get("scopes", [])
        
        if not isinstance(scopes, list):
            logger.error(f"Token scopes is not a list: {type(scopes)}")
            return False
        
        scopes = [s for s in scopes if isinstance(s, str)]
        
        result = required_scope in scopes
        
        if not result:
            logger.debug(f"Required scope '{required_scope}' not found in token scopes: {scopes}")
        
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error checking scope: {str(e)}")
        return False


def get_required_scope(
    method: str,
    tool_name: str | None = None,
) -> str:
    """
    Determine the authorization scope required for an MCP request.
 
    Args:
        method: The MCP method being called
        tool_name: The tool name if method is tools/call, otherwise None
 
    Returns:
        "none"  -> authentication required, but no scope check
        "read"  -> read scope required
        "write" -> write scope required
        "deny"  -> unknown/unsupported operation
    """
    try:
        if not isinstance(method, str):
            logger.error(f"Invalid method type: expected str, got {type(method)}")
            return "deny"
            
        if not method or not method.strip():
            logger.warning("Method cannot be empty")
            return "deny"
        
        method = method.strip()
 
        if method == "initialize":
            return "none"
 
        if method in READ_MCP_METHODS:
            return "read"
 
        if method == "tools/call":
            
            if tool_name is None:
                logger.warning("Tool name is None for tools/call method")
                return "deny"
                
            if not isinstance(tool_name, str):
                logger.error(f"Invalid tool_name type: expected str, got {type(tool_name)}")
                return "deny"
                
            tool_name = tool_name.strip()
            
            if not tool_name:
                logger.warning("Tool name is empty for tools/call method")
                return "deny"
 
            if tool_name in READ_TOOLS:
                return "read"
 
            if tool_name in WRITE_TOOLS:
                return "write"
 
            logger.warning(f"Unknown tool requested: {tool_name}")
            return "deny"
 
        logger.warning(f"Unknown MCP method: {method}")
        return "deny"
        
    except Exception as e:
        logger.error(f"Unexpected error determining required scope: {str(e)}")
        return "deny"