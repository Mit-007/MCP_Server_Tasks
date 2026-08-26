from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.server.dependencies import get_http_headers
from starlette.exceptions import HTTPException
from src.tasks_mcp_server.task_2.auth.token_auth import (verify_token,check_token_expiry)
from src.tasks_mcp_server.task_2.auth.scope_auth import (get_required_scope,check_scope)
from src.tasks_mcp_server.task_2.core.logger import logger
import os


# --------------------------------------------------
# Logger configuration
# --------------------------------------------------        

class AuthenticationMiddleware(Middleware):
 
    def __init__(self):
        logger.info("Authentication middleware initialized")
 
    async def on_request(
        self,
        context: MiddlewareContext,
        call_next,
    ):
        """
        Authenticate the request and authorize the requested operation.
        """
 
        try:
            logger.info("========== AUTHENTICATION REQUEST ==========")
            logger.info(context)
            logger.info("-------------------------------------------")
 
            # --------------------------------------------------
            # 1. Get HTTP Authorization header
            # --------------------------------------------------
            try:
                headers = get_http_headers()
                logger.info(f"Header : {headers}")
                authorization_token = headers.get("auth_token")
 
                logger.info(
                    "Authorization header present: %s",
                    authorization_token is not None,
                )
 
                if not authorization_token:
                    transport_mode = str(os.getenv("TRANSPORT_TYPE_JOB_SERVER")).strip().upper()
                    logger.info(f"transport type : {transport_mode}")
                    if transport_mode == "STDIO":
                        authorization_token = str(os.getenv("AUTH_TOKEN")).strip()
                        logger.info(f"auth_token from env: {authorization_token}")
                        if not authorization_token:
                            raise HTTPException(
                                status_code=401,
                                detail={
                                    "error" : "missing Authetication Token in env for STDIO",
                                    "code" : "MISSING_TOKEN_ENV",
                                    "suggestion" : "Provide Authorization TOKEN in environment for STDIO transport",
                                }
                            )
                    else:
                        raise HTTPException(
                            status_code=401,
                            detail={
                                "error": "Missing authentication token",
                                "code": "MISSING_TOKEN",
                                "suggestion": "Provide Authorization header or set AUTH_TOKEN in environment for STDIO transport"
                            }
                        )
                        
            except HTTPException as http_err:
                raise http_err
            except Exception as e:
                logger.error(f"Error extracting headers: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "Failed to extract authentication headers",
                        "code": "HEADER_EXTRACTION_ERROR",
                        "suggestion": "Contact server administrator if problem persists"
                    }
                )
             
            # --------------------------------------------------
            # 2. Verify token
            # --------------------------------------------------
            try:
                token_info, error = verify_token(authorization_token)
                
                if token_info is None:
                    logger.warning("Token verification failed")
                    raise HTTPException(
                        status_code=401,
                        detail={
                            "error": error or "Invalid authentication token",
                            "code": "INVALID_TOKEN",
                            "suggestion": "Verify your token is correct and try again"
                        }
                    )
 
                logger.info("Token verification successful")
                
            except HTTPException as http_err:
                raise http_err
            except Exception as e:
                logger.error(f"Unexpected error during token verification: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "Token verification failed unexpectedly",
                        "code": "TOKEN_VERIFICATION_ERROR",
                        "suggestion": "Contact server administrator if problem persists"
                    }
                )
 
            # --------------------------------------------------
            # 3. Check token expiry
            # --------------------------------------------------
            try:
                is_valid, expired_seconds = check_token_expiry(token_info)
 
                if not is_valid:
                    logger.warning(
                        "Token expired %s seconds ago",
                        expired_seconds,
                    )
                    raise HTTPException(
                        status_code=401,
                        detail={
                            "error": f"Token expired {expired_seconds} seconds ago",
                            "code": "TOKEN_EXPIRED",
                            "suggestion": "Request a new authentication token"
                        }
                    )
 
                logger.info("Token expiry check successful")
                
            except HTTPException as http_err:
                raise http_err
            except Exception as e:
                logger.error(f"Unexpected error during token expiry check: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "Token expiry check failed unexpectedly",
                        "code": "TOKEN_EXPIRY_CHECK_ERROR",
                        "suggestion": "Contact server administrator if problem persists"
                    }
                )
 
            # --------------------------------------------------
            # 4. Get MCP method
            # --------------------------------------------------
            try:
                method = self._get_method(context)
 
                logger.info(
                    "MCP method: %s",
                    method,
                )
                
            except Exception as e:
                logger.error(f"Error extracting MCP method: {str(e)}")
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": "Failed to extract MCP method from request",
                        "code": "METHOD_EXTRACTION_ERROR",
                        "suggestion": "Verify request structure is valid"
                    }
                )
 
            # --------------------------------------------------
            # 5. Get tool name
            # --------------------------------------------------
            try:
                tool_name = None
 
                if method == "tools/call":
                    tool_name = self._get_tool_name(context)
 
                logger.info(
                    "Tool name: %s",
                    tool_name,
                )
                
            except Exception as e:
                logger.error(f"Error extracting tool name: {str(e)}")
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": "Failed to extract tool name from request",
                        "code": "TOOL_NAME_EXTRACTION_ERROR",
                        "suggestion": "Verify tool call request structure is valid"
                    }
                )
 
            # --------------------------------------------------
            # 6. Determine required scope
            # --------------------------------------------------
            try:
                required_scope = get_required_scope(
                    method=method,
                    tool_name=tool_name,
                )
 
                logger.info(
                    "Required scope: %s",
                    required_scope,
                )
                
            except Exception as e:
                logger.error(f"Error determining required scope: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "Failed to determine required scope for operation",
                        "code": "SCOPE_DETERMINATION_ERROR",
                        "suggestion": "Contact server administrator if problem persists"
                    }
                )
 
            # --------------------------------------------------
            # 7. Reject unknown operations
            # --------------------------------------------------
 
            if required_scope == "deny":
                logger.warning(
                    "Authorization denied: unknown operation "
                    "(method=%s, tool=%s)",
                    method,
                    tool_name,
                )
                raise HTTPException(
                    status_code=403,
                    detail={
                        "error": "Operation is not authorized",
                        "code": "OPERATION_NOT_AUTHORIZED",
                        "suggestion": f"Method '{method}' with tool '{tool_name}' is not supported"
                    }
                )
 
            # --------------------------------------------------
            # 8. No scope required
            # --------------------------------------------------
 
            if required_scope == "none":
                logger.info(
                    "No scope check required for method: %s",
                    method,
                )
 
                return await call_next(context)
 
            # --------------------------------------------------
            # 9. Check scope
            # --------------------------------------------------
            try:
                token_scopes = token_info.get("scopes", [])
 
                logger.debug(
                    "Token scopes: %s",
                    token_scopes,
                )
 
                if not check_scope(
                    token_info,
                    required_scope,
                ):
                    logger.warning(
                        "Authorization denied: insufficient scope "
                        "(method=%s, tool=%s, required=%s, "
                        "token_scopes=%s)",
                        method,
                        tool_name,
                        required_scope,
                        token_scopes,
                    )
 
                    raise HTTPException(
                        status_code=403,
                        detail={
                            "error": f"Insufficient scope. Required scope: {required_scope}",
                            "code": "INSUFFICIENT_SCOPE",
                            "suggestion": f"Your token needs '{required_scope}' scope but has {token_scopes}"
                        }
                    )
                    
            except HTTPException as http_err:
                raise http_err
            except Exception as e:
                logger.error(f"Unexpected error during scope check: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "Scope validation failed unexpectedly",
                        "code": "SCOPE_CHECK_ERROR",
                        "suggestion": "Contact server administrator if problem persists"
                    }
                )
 
            # --------------------------------------------------
            # 10. Authorized
            # --------------------------------------------------
 
            logger.info(
                "Authorization successful "
                "(method=%s, tool=%s, scope=%s)",
                method,
                tool_name,
                required_scope,
            )
 
            logger.info("============================================")
 
            return await call_next(context)
            
        except HTTPException as http_err:
            raise http_err
        except Exception as e:
            logger.error(f"Unexpected error in authentication middleware: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Authentication middleware encountered an unexpected error",
                    "code": "MIDDLEWARE_ERROR",
                    "suggestion": "Contact server administrator if problem persists"
                }
            )



    def _get_method(
        self,
        context: MiddlewareContext,
    ) -> str:
        """
        Get the MCP request method from the middleware context.
        """
        try:
            method = context.method
            
            if not method:
                raise ValueError("Method is empty or None")
                
            return method
            
        except AttributeError as e:
            raise ValueError(f"Failed to extract method from context: {str(e)}")
        except Exception as e:
            raise ValueError(f"Unexpected error extracting method: {str(e)}")
 
    def _get_tool_name(
        self,
        context: MiddlewareContext,
    ) -> str | None:
        """
        Get the tool name when the request is tools/call.
        """
 
        if context.method != "tools/call":
            return None
 
        try:
            if not hasattr(context, 'message'):
                raise AttributeError("Context has no message attribute")
                
            if not hasattr(context.message, 'name'):
                raise AttributeError("Message has no name attribute")
                
            tool_name = context.message.name
 
            logger.debug(
                "Extracted tool name: %s",
                tool_name,
            )
 
            return tool_name
            
        except AttributeError as e:
            logger.error(f"Error extracting tool name: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error extracting tool name: {str(e)}")
            return None