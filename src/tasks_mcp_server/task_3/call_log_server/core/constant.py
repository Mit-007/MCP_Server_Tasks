from typing import Literal
from typing import get_args

# lenght of auth token 
length_of_token = 32

# --> Available scope for authorization
Available_scope = Literal["read", "write"]

VALID_SCOPES = set(get_args(Available_scope))

# -->read scope tools
READ_TOOLS = {
    "call_log_server_get_call",
    "call_log_server_list_calls",
    "call_log_server_list_calls_by_status",
    "call_log_server_list_notes_for_call",
    "call_log_server_get_stats"
}

# --> write scope tools
WRITE_TOOLS = {
    "call_log_server_log_call",
    "call_log_server_update_call_outcome",
    "call_log_server_delete_call",
    "call_log_server_add_call_note",
    "call_log_server_get_call_summary"
}

# --> read scope methods
READ_MCP_METHODS = {
    "tools/list",
    "resources/list",
    "resources/read",
    "prompts/list",
    "prompts/get",
    "resources/templates/list",
}
