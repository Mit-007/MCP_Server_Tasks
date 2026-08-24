import asyncio
import json
import time
from langchain_core.messages import (
    HumanMessage,
    ToolMessage,
)
from src.tasks_mcp_server.task_3.agent.services.llm import llm
from src.tasks_mcp_server.task_3.agent.services.tools import get_tools
from src.tasks_mcp_server.task_3.agent.core.logger import logger
from src.tasks_mcp_server.task_3.agent.services.prompt import get_prompt

# ============================================================
# Calculate response size
# ============================================================

def get_response_size_bytes(response):

    try:
        serialized = json.dumps(
            response,
            default=str,
            ensure_ascii=False,
        )

        return len(
            serialized.encode("utf-8")
        )

    except Exception:

        return len(
            str(response).encode("utf-8")
        )


# ============================================================
# Identify tool type (MCP or Workflow)
# ============================================================

def identify_tool_type(tool_name: str) -> str:
    """
    Determine if tool is a Workflow tool or MCP tool
    Workflow tools start with 'wf'
    """
    if tool_name.startswith("wf"):
        return "WORKFLOW"
    elif tool_name.startswith("job_server"):
        return "MCP_JOB_SERVER"
    elif tool_name.startswith("call_log_server"):
        return "MCP_CALL_LOG_SERVER"
    else:
        return "MCP_OTHER"


# ============================================================
# Main
# ============================================================

async def main():

    logger.info("Start the program")

    # get all tools
    tools, tool_by_name = await get_tools()

    if not tools:
        logger.error("MCP servers are not connected!")
        return

    # bind tools
    llm_with_tools = llm.bind_tools(tools)

    messages = []

    # --------------------------------------------------------
    # Chat loop
    # --------------------------------------------------------

    while True:

        question = input("\n👨 Enter your question: ")

        if question.lower() in ["exit", "quit"]:
            print("Exiting...")
            break

        # Add HumanMessage
        messages.append(HumanMessage(content=question))

        try:
            # get prompt
            prompt = get_prompt(messages)

            # Call LLM
            response = await llm_with_tools.ainvoke(messages)

            messages.append(response)

            # ------------------------------------------------
            # Tool execution loop
            # ------------------------------------------------

            while response.tool_calls:

                for tool_call in response.tool_calls:

                    tool_name = tool_call["name"]
                    tool_args = tool_call["args"]
                    tool_call_id = tool_call["id"]


                    # Get tool
                    tool = tool_by_name.get(tool_name)

                    if tool is None:

                        logger.error("Tool not found: %s",tool_name,)

                        messages.append(
                            ToolMessage(
                                content=(
                                    f"Tool '{tool_name}' "
                                    f"not found."
                                ),
                                tool_call_id=tool_call_id,
                            )
                        )

                        continue

                    # Identify tool type
                    tool_type = identify_tool_type(tool_name)

            
                    # Determine server name (for MCP tools)
                    server_name = "unknown"

                    if tool_type == "MCP_JOB_SERVER":
                        server_name = "job_server"
                    elif tool_type == "MCP_CALL_LOG_SERVER":
                        server_name = "call_log_server"
                    elif tool_type == "WORKFLOW":
                        server_name = "workflows"


                    # Print tool information
                    if tool_type == "WORKFLOW":
                        print(
                            f"\n⚙️  [WORKFLOW] Executing: {tool_name}"
                        )
                        print(
                            f"   Arguments: {tool_args}"
                        )
                    else:
                        print(
                            f"\n🔧 [MCP] Calling tool: {tool_name}"
                        )
                        print(
                            f"   Server: {server_name}"
                        )
                        print(
                            f"   Arguments: {tool_args}"
                        )

                    # Start timer
                    start_time = time.perf_counter()

                    try:
                        # start tool execution

                        result = await tool.ainvoke(tool_args)

                        # Calculate latency
                        latency_ms = (
                            time.perf_counter()
                            - start_time
                        ) * 1000


                        # Calculate response size
                        response_size_bytes = (
                            get_response_size_bytes(result)
                        )


                        print(f"🔧 Tool Result: {result}")


                        # Log tool call

                        if tool_type == "WORKFLOW":
                            logger.info(
                                "WORKFLOW EXECUTION | "
                                "tool=%s | "
                                "args=%s | "
                                "latency_ms=%.2f | "
                                "response_size_bytes=%d | "
                                "status=success",
                                tool_name,
                                tool_args,
                                latency_ms,
                                response_size_bytes,
                            )
                        else:
                            logger.info(
                                "MCP TOOL CALL | "
                                "server=%s | "
                                "tool=%s | "
                                "args=%s | "
                                "latency_ms=%.2f | "
                                "response_size_bytes=%d | "
                                "status=success",
                                server_name,
                                tool_name,
                                tool_args,
                                latency_ms,
                                response_size_bytes,
                            )


                        # Add ToolMessage
                        messages.append(
                            ToolMessage(
                                content=str(result),
                                tool_call_id=tool_call_id,
                            )
                        )

                    except Exception as e:


                        # Calculate latency for failed call
                        latency_ms = (
                            time.perf_counter()
                            - start_time
                        ) * 1000


                        # Log failed tool call
                        if tool_type == "WORKFLOW":
                            logger.exception(
                                "WORKFLOW EXECUTION | "
                                "tool=%s | "
                                "args=%s | "
                                "latency_ms=%.2f | "
                                "response_size_bytes=0 | "
                                "status=error | "
                                "error=%s",
                                tool_name,
                                tool_args,
                                latency_ms,
                                str(e),
                            )
                        else:
                            logger.exception(
                                "MCP TOOL CALL | "
                                "server=%s | "
                                "tool=%s | "
                                "args=%s | "
                                "latency_ms=%.2f | "
                                "response_size_bytes=0 | "
                                "status=error | "
                                "error=%s",
                                server_name,
                                tool_name,
                                tool_args,
                                latency_ms,
                                str(e),
                            )


                        # Add error ToolMessage
                        messages.append(
                            ToolMessage(
                                content=(
                                    f"Tool execution failed: "
                                    f"{str(e)}"
                                ),
                                tool_call_id=tool_call_id,
                            )
                        )

                # ------------------------------------------------
                # Send updated history back to LLM
                # ------------------------------------------------

                response = await llm_with_tools.ainvoke(messages)

                # Add AIMessage
                messages.append(response)

            # ------------------------------------------------
            # Final AI response
            # ------------------------------------------------
            print("\n\n----------------")
            print("|✅ Output :-  |")
            print("----------------")
            print("\nAI:",response.content[0]["text"])

        except Exception as e:
            logger.exception("Error while processing user request")
            print(f"\nError: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())