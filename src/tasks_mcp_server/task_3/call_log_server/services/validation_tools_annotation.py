from src.tasks_mcp_server.task_2.core.logger import logger

async def validate_tool_annotations(mcp):
    """Validate that tool annotations follow constraints."""
    tools = await mcp.list_tools()

    for tool in tools:
        annotations = tool.annotations

        destructive = annotations.destructiveHint if annotations else False
        idempotent = annotations.idempotentHint if annotations else False

        if destructive and idempotent:
            raise AssertionError(
                f"Tool '{tool.name}' has "
                f"destructiveHint=true and idempotentHint=true."
            )


    logger.info("Tool annotation validation passed")