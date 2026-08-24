from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.server.dependencies import get_http_headers
from starlette.exceptions import HTTPException
from src.tasks_mcp_server.task_3.call_log_server.auth.token_auth import (verify_token,check_token_expiry)
from src.tasks_mcp_server.task_3.call_log_server.auth.scope_auth import (get_required_scope,check_scope)
from src.tasks_mcp_server.task_3.call_log_server.core.logger import logger
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

        logger.info("========== AUTHENTICATION REQUEST ==========")
        logger.info(context)
        logger.info("-------------------------------------------")

        # --------------------------------------------------
        # 1. Get HTTP Authorization header
        # --------------------------------------------------

        headers = get_http_headers()
        logger.info(f"Header : {headers}")
        authorization_token = headers.get("auth_token")

        logger.info(
            "Authorization header present: %s",
            authorization_token is not None,
        )

        # Never log the actual token.
        if not authorization_token:
            transport_mode = str(os.getenv("TRANSPORT_TYPE")).strip()
            logger.info(f"transpport type : {transport_mode}")
            if transport_mode == "STDIO":
                authorization_token = str(os.getenv("AUTH_TOKEN")).strip()
                logger.info(f"auth_token_ : {authorization_token}")

            else :
                raise Exception
         
        # --------------------------------------------------
        # 2. Verify token
        # --------------------------------------------------
        
        
        token_info , error = verify_token(authorization_token)
        
        if token_info is None:
            
            logger.warning("Token verification failed")

            raise HTTPException(
                status_code=401,
                detail=error,
            )

        logger.info("Token verification successful")

        # --------------------------------------------------
        # 3. Check token expiry
        # --------------------------------------------------

        is_valid, expired_seconds = check_token_expiry(
            token_info
        )

        if not is_valid:
            logger.warning(
                "Token expired %s seconds ago",
                expired_seconds,
            )

            raise HTTPException(
                status_code=401,
                detail=(
                    f"Token expired "
                    f"{expired_seconds} seconds ago"
                ),
            )

        logger.info("Token expiry check successful")

        # --------------------------------------------------
        # 4. Get MCP method
        # --------------------------------------------------

        method = self._get_method(context)

        logger.info(
            "MCP method: %s",
            method,
        )

        # --------------------------------------------------
        # 5. Get tool name
        # --------------------------------------------------

        tool_name = None

        if method == "tools/call":
            tool_name = self._get_tool_name(context)

        logger.info(
            "Tool name: %s",
            tool_name,
        )

        # --------------------------------------------------
        # 6. Determine required scope
        # --------------------------------------------------

        required_scope = get_required_scope(
            method=method,
            tool_name=tool_name,
        )

        logger.info(
            "Required scope: %s",
            required_scope,
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
                detail="Operation is not authorized",
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
                detail=(
                    f"Insufficient scope. "
                    f"Required scope: {required_scope}"
                ),
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



    def _get_method(
        self,
        context: MiddlewareContext,
    ) -> str:
        """
        Get the MCP request method from the middleware context.
        """

        method = context.method

        return method

    def _get_tool_name(
        self,
        context: MiddlewareContext,
    ) -> str | None:
        """
        Get the tool name when the request is tools/call.
        """

        if context.method != "tools/call":
            return None

        tool_name = context.message.name

        logger.debug(
            "Extracted tool name: %s",
            tool_name,
        )

        return tool_name