from fastmcp import FastMCP
from fastmcp.server.transforms import Namespace
from src.tasks_mcp_server.task_2.middleware.middaleware import AuthenticationMiddleware
from src.tasks_mcp_server.task_2.core.config import TRANSPORT_TYPE,TRANSPORT_PORT
from src.tasks_mcp_server.task_2.prompts import prompts 
from src.tasks_mcp_server.task_2.resources import (job_resources, technicians_resources)
from src.tasks_mcp_server.task_2.tools import (read_tool, write_tool)


# ---> create Mcp server
mcp =FastMCP("Task-2")
mcp.add_middleware(AuthenticationMiddleware())


## ----> Add primitives

# Tools
read_tool.register_read_tools(mcp)
write_tool.register_write_tool(mcp)

# resources
job_resources.register_job_resources(mcp)
technicians_resources.register_technicians_resources(mcp)

#prompts
prompts.register_prompts(mcp)

mcp.add_transform(Namespace("job_server"))

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
    