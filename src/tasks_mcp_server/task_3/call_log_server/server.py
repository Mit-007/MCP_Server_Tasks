from fastmcp import FastMCP
from fastmcp.server.transforms import Namespace
from src.tasks_mcp_server.task_3.call_log_server.middleware.middleware import AuthenticationMiddleware
from src.tasks_mcp_server.task_3.call_log_server.core.config import TRANSPORT_TYPE,TRANSPORT_PORT
from src.tasks_mcp_server.task_3.call_log_server.prompts import prompts 
from src.tasks_mcp_server.task_3.call_log_server.resources import resources
from src.tasks_mcp_server.task_3.call_log_server.tools import tools


# ---> create Mcp server
mcp =FastMCP("Task-3_call_log_server")
mcp.add_middleware(AuthenticationMiddleware())


## ----> Add primitives

# Tools
tools.register_tools(mcp)

# resources
resources.register_resources(mcp)

#prompts
prompts.register_prompts(mcp)

mcp.add_transform(Namespace("call_log_server"))

# ---> run mcp server
if __name__ ==  "__main__" :

    try:
        if TRANSPORT_TYPE == "HTTP":

            if not TRANSPORT_PORT:
                raise ValueError("TRANSPORT_PORT must be provided for HTTP transport")
            
            else :
                mcp.run(transport="http", host="0.0.0.0", port=TRANSPORT_PORT)

        else:
            mcp.run(transport="stdio")
    except Exception:
        raise
    