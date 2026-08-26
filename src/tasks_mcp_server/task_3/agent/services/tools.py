from src.tasks_mcp_server.task_3.agent.mcp_clients import get_mcp_servers_tools
from src.tasks_mcp_server.task_3.agent.services.workflows_tools import WorkflowToolsRegistry
import asyncio

async def get_tools():
    """
    Get all tools: MCP tools + Workflow tools
    """
    
    # Step 1: Get MCP server tools
    print("\n" + "="*60)
    print("Loading MCP Server Tools...")
    print("="*60 + "\n")
    
    mcp_tools = await get_mcp_servers_tools()
    
    tool_by_name = {}
    
    print("\n[MCP TOOLS - Available]:\n")
    for tool in mcp_tools:
        print(f"  ✓ {tool.name}")
        tool_by_name[tool.name] = tool
    
    # Step 2: Create workflow tools registry (pass MCP tools)
    print("\n" + "="*30)
    print("Loading Workflow Tools...")
    print("="*30 + "\n")
    
    workflow_registry = WorkflowToolsRegistry(tool_by_name)
    workflow_tools = workflow_registry.get_workflow_tools()
    workflow_tools_dict = workflow_registry.get_workflow_tools_dict()
    
    print("\n[WORKFLOW TOOLS - Available]:\n")
    for wf_name, wf_tool in workflow_tools_dict.items():
        print(f"  ⚙ {wf_name}")
        tool_by_name[wf_name] = wf_tool
    
    # Step 3: Combine all tools
    print("\n" + "="*30)
    print("Tool Summary")
    print("="*30)
    print(f"  MCP Tools:      {len(mcp_tools)}")
    print(f"  Workflow Tools: {len(workflow_tools)}")
    print(f"  Total:          {len(tool_by_name)}\n")
    
    all_tools = mcp_tools + workflow_tools
    
    return all_tools, tool_by_name

if __name__ == "__main__":
    mcp_tools, tool_by_name = asyncio.run(get_tools())
