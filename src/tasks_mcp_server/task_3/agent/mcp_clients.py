from langchain_mcp_adapters.client import MultiServerMCPClient

SERVERS = {
    "Task-2": {
        "transport": "streamable_http",
        "url": "http://localhost:3001/mcp",
        "headers": {
            "AUTH_TOKEN": "Bearer dddgN6MH20Kx9fjJ5W50JCDaKjpxsS1p",
        },
    },

    "Task-3_call_log_server": {
        "transport": "streamable_http",
        "url": "http://localhost:3000/mcp",
        "headers": {
            "AUTH_TOKEN": "Bearer dddgN6MH20Kx9fjJ5W50JCDaKjpxsS1p",
        },
    },
}

async def get_mcp_servers_tools():
    client = MultiServerMCPClient(SERVERS)
    
    tools = await client.get_tools()

    return tools