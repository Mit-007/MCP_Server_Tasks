from langchain_mcp_adapters.client import MultiServerMCPClient
from src.tasks_mcp_server.task_3.agent.core.server_config import SERVERS
from src.tasks_mcp_server.task_3.agent.core.logger import logger


async def get_mcp_servers_tools():
    all_tools = []

    for server_name, server_config in SERVERS.items():
        try:
            logger.info(f"Connecting to MCP server: {server_name}")

            client = MultiServerMCPClient({
                server_name: server_config
            })

            tools = await client.get_tools()

            all_tools.extend(tools)

            logger.info(f"Successfully connected to {server_name}")

        except Exception as e:
            logger.error(f"Failed to connect to MCP server '{server_name}': {e}")
            continue

    if not all_tools:
        logger.error("No MCP servers could be connected.")
        raise ConnectionError("Failed to connect to all MCP servers.")

    logger.info(
        f"Successfully loaded {len(all_tools)} tools "
        f"from available MCP servers"
    )

    return all_tools