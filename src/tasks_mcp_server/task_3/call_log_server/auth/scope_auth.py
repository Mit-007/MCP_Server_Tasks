VALID_SCOPES = {
    "read",
    "write",
}


READ_TOOLS = {
    "call_log_server_get_call",
    "call_log_server_list_calls",
    "call_log_server_list_calls_by_status",
    "call_log_server_list_notes_for_call",
    "call_log_server_get_stats"
}


WRITE_TOOLS = {
    "call_log_server_log_call",
    "call_log_server_update_call_outcome",
    "call_log_server_delete_call",
    "call_log_server_add_call_note",
    "call_log_server_get_call_summary"
}


READ_MCP_METHODS = {
    "tools/list",
    "resources/list",
    "resources/read",
    "prompts/list",
    "prompts/get",
    "resources/templates/list",
}


def validate_scope(scope: str) -> bool:
    """
    Check whether a scope is supported by the authorization system.
    """

    return scope in VALID_SCOPES


def check_scope(
    token_info: dict,
    required_scope: str,
) -> bool:
    """
    Check whether the authenticated token has the required scope.
    """

    if not validate_scope(required_scope):
        return False

    scopes = token_info.get("scopes", [])

    return required_scope in scopes


def get_required_scope(
    method: str,
    tool_name: str | None = None,
) -> str:
    """
    Determine the authorization scope required for an MCP request.

    Returns:
        "none"  -> authentication required, but no scope check
        "read"  -> read scope required
        "write" -> write scope required
        "deny"  -> unknown/unsupported operation
    """

    # Session initialization.
    if method == "initialize":
        return "none"

    # MCP read operations.
    if method in READ_MCP_METHODS:
        return "read"

    # Tool execution.
    if method == "tools/call":

        if tool_name in READ_TOOLS:
            return "read"

        if tool_name in WRITE_TOOLS:
            return "write"

        # Unknown tool.
        return "deny"

    # Unknown MCP method.
    return "deny"