from typing import Literal
from typing import get_args

# lenght of auth token 
length_of_token = 32

# --> Available scope for authorization
Available_scope = Literal["read", "write"]

VALID_SCOPES = set(get_args(Available_scope))

# -->read scope tools
READ_TOOLS = {
    "job_server_list_jobs",
    "job_server_list_technicians",
    "job_server_get_available_technicians",
    "job_server_open_jobs",
}

# --> write scope tools
WRITE_TOOLS = {
    "job_server_create_job",
    "job_server_assign_job",
    "job_server_update_job",
    "job_server_delete_job",
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