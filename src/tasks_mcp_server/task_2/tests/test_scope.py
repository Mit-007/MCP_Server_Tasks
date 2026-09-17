import pytest
from src.tasks_mcp_server.task_2.auth.scope_auth import check_scope, validate_scope, get_required_scope


class TestScopeAuth:
    """Test scope authorization functions."""
    
    
    @pytest.mark.parametrize(
        "scope, expected",
        [
            ("read", True),
            ("write", True),
            ("delete", False),
            ("", False),
            ("   ", False),
            (123, False),
        ],
    )
    def test_validate_scope(self,scope, expected):
        """Test scope validation for valid and invalid inputs."""

        result = validate_scope(scope)

        assert result is expected

    
    @pytest.mark.parametrize(
        "token_info, required_scope, expected",
        [
            ({"scopes": ["read", "write"]}, "read", True),
            ({"scopes": ["read"]}, "write", False),
            ({"scopes": []}, "read", False),
            ("not_a_dict", "read", False),
            ({"scopes": ["read"]}, 123, False),
            ({"scopes": ["read", "write"]}, "invalid", False),
        ],
        ids=[
            "valid_scope",
            "missing_scope",
            "empty_scopes",
            "invalid_token_info_type",
            "invalid_required_scope_type",
            "invalid_required_scope_value",
        ],
    )
    def test_check_scope(self, token_info, required_scope, expected):
        result = check_scope(token_info, required_scope)

        assert result is expected

        
    @pytest.mark.parametrize(
        "method, tool_name, expected",
        [
            ("initialize", None, "none"),
            ("tools/list", None, "read"),
            ("resources/list", None, "read"),
            ("tools/call", "job_server_list_jobs", "read"),
            ("tools/call", "job_server_create_job", "write"),
            ("unknown/method", None, "deny"),
            ("tools/call", None, "deny"),
            ("tools/call", "unknown_tool", "deny"),
            (123, None, "deny"),
        ],
        ids=[
            "initialize",
            "tools_list",
            "resources_list",
            "read_tool",
            "write_tool",
            "unknown_method",
            "tools_call_without_tool",
            "unknown_tool",
            "invalid_method_type",
        ],
    )
    def test_get_required_scope(self, method, tool_name, expected):
        """Test required scope for different MCP methods and tools."""

        scope = get_required_scope(method, tool_name)

        assert scope == expected