from langchain_mcp_adapters.client import MultiServerMCPClient
from src.tasks_mcp_server.task_3.agent.core.server_config import SERVERS
from src.tasks_mcp_server.task_3.agent.core.logger import logger

async def get_mcp_servers_tools():
    try:
        client = MultiServerMCPClient(SERVERS)

        logger.info("Connected to MCP servers sucessfully.")

        tools = await client.get_tools()

        logger.info(f"Successfully loaded {len(tools)} tools from MCP servers")

        return tools
    
    except ConnectionError as e:
        logger.error(f"Failed to connect to MCP servers: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to load MCP tools: {e}")
        raise