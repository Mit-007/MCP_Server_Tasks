import pytest
from fastmcp import FastMCP
from src.tasks_mcp_server.task_2.schemas.tool_input_schemas import (
    PaginationInput,
)
from src.tasks_mcp_server.task_2.data import data as D


@pytest.fixture(autouse=True)
def reset_state():
    """Reset data before each test."""
    D.jobs.clear()
    D.technicians.clear()
    
    D.jobs.extend([
        {"id": "JOB-001", "title": "Job 1", "status": "open", "description": "Desc", "priority": "high", "technician_id": None},
        {"id": "JOB-002", "title": "Job 2", "status": "open", "description": "Desc", "priority": "high", "technician_id": None},
        {"id": "JOB-003", "title": "Job 3", "status": "open", "description": "Desc", "priority": "high", "technician_id": None},
        {"id": "JOB-004", "title": "Job 4", "status": "open", "description": "Desc", "priority": "high", "technician_id": None},
        {"id": "JOB-005", "title": "Job 5", "status": "open", "description": "Desc", "priority": "high", "technician_id": None},
    ])
    
    D.technicians.extend([
        {"id": "TECH-001", "name": "Tech 1", "available": True, "skills": ["ac", "refrigerator"]},
        {"id": "TECH-002", "name": "Tech 2", "available": True, "skills": ["washing-machine"]},
        {"id": "TECH-003", "name": "Tech 3", "available": False, "skills": ["microwave"]},
    ])
    
    yield
    D.jobs.clear()
    D.technicians.clear()

@pytest.fixture
def mcp_server():
    """Create a FastMCP server with read tools registered."""

    from src.tasks_mcp_server.task_2.tools.read_tool import (
        register_read_tools,
    )

    mcp = FastMCP("test")

    register_read_tools(mcp)

    return mcp


async def get_tool(mcp: FastMCP, tool_name: str):
    """Get a registered FastMCP tool."""

    return await mcp.get_tool(tool_name)


class TestReadTools:
    """Test read tool functions."""

    @pytest.mark.asyncio
    async def test_list_jobs_first_page(self, mcp_server):
        """Test listing jobs first page."""

        pagination = PaginationInput(
            cursor="0",
            limit=2,
        )

        tool = await get_tool(
            mcp_server,
            "list_jobs",
        )

        assert tool is not None

        result = await tool.fn(pagination)

        assert result is not None
        assert result.data is not None
        assert len(result.data) <= 2
        assert result.pagination.has_more is not None

    @pytest.mark.asyncio
    async def test_list_jobs_beyond_data(self, mcp_server):
        """Test listing jobs beyond available data."""

        pagination = PaginationInput(
            cursor="100",
            limit=10,
        )

        tool = await get_tool(
            mcp_server,
            "list_jobs",
        )

        assert tool is not None

        result = await tool.fn(pagination)

        assert result is not None
        assert result.data is not None
        assert len(result.data) == 0
        assert result.pagination.has_more is False

    @pytest.mark.asyncio
    async def test_list_jobs_negative_cursor(self, mcp_server):
        """Test listing jobs with negative cursor."""

        pagination = PaginationInput(
            cursor="-1",
            limit=10,
        )

        tool = await get_tool(
            mcp_server,
            "list_jobs",
        )

        assert tool is not None

        result = await tool.fn(pagination)

        assert result is not None

        # Depending on implementation, a negative cursor
        # may return an error response or an empty result.
        assert (
            hasattr(result, "error")
            or len(result.data) == 0
        )

    @pytest.mark.asyncio
    async def test_list_technicians_first_page(self, mcp_server):
        """Test listing technicians first page."""

        pagination = PaginationInput(
            cursor="0",
            limit=2,
        )

        tool = await get_tool(
            mcp_server,
            "list_technicians",
        )

        assert tool is not None

        result = await tool.fn(pagination)

        assert result is not None
        assert result.data is not None
        assert len(result.data) <= 2

    @pytest.mark.asyncio
    async def test_get_available_technicians(self, mcp_server):
        """Test getting available technicians."""

        pagination = PaginationInput(
            cursor="0",
            limit=10,
        )

        tool = await get_tool(
            mcp_server,
            "get_available_technicians",
        )

        assert tool is not None

        result = await tool.fn(pagination)

        assert result is not None
        assert result.data is not None

        for tech in result.data:
            assert tech.available is True

    @pytest.mark.asyncio
    async def test_open_jobs(self, mcp_server):
        """Test getting open jobs."""

        pagination = PaginationInput(
            cursor="0",
            limit=10,
        )

        tool = await get_tool(
            mcp_server,
            "open_jobs",
        )

        assert tool is not None

        result = await tool.fn(pagination)

        assert result is not None
        assert result.data is not None

        for job in result.data:
            assert job.status == "open"