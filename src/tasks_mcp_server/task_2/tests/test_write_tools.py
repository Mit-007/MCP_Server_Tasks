import pytest
from fastmcp import FastMCP
from src.tasks_mcp_server.task_2.data import data as D
from src.tasks_mcp_server.task_2.schemas.tool_input_schemas import (
    CreateJobInput,
    AssignJobInput,
    UpdateJobInput,
    DeleteJobInput,
    Priority,
    JobStatus,
)
from src.tasks_mcp_server.task_2.schemas.error_schemas import ErrorResponse
from src.tasks_mcp_server.task_2.services.validation_services import get_job


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
    """Create a FastMCP server with write tools registered."""

    from src.tasks_mcp_server.task_2.tools.write_tool import (
        register_write_tool,
    )

    mcp = FastMCP("test")

    register_write_tool(mcp)

    return mcp


async def get_tool(mcp: FastMCP, tool_name: str):
    """Get a registered FastMCP tool."""

    return await mcp.get_tool(tool_name)


class TestWriteTools:
    """Test write tool functions."""

    # ============================================================
    # CREATE JOB
    # ============================================================

    @pytest.mark.asyncio
    async def test_create_job_success(self, mcp_server):
        """Test creating a new job."""

        tool = await get_tool(
            mcp_server,
            "create_job",
        )

        job_input = CreateJobInput(
            id="JOB-NEW",
            title="New Job",
            description="Test job description",
            priority=Priority.HIGH,
        )

        result = await tool.fn(job_input)

        assert result is not None

        assert result.job is not None

        assert result.job.id == "JOB-NEW"
        assert result.job.title == "New Job"
        assert result.job.description == "Test job description"

        assert result.job.priority == Priority.HIGH.value

    @pytest.mark.asyncio
    async def test_create_job_duplicate(self, mcp_server):
        """Test creating job with duplicate ID."""

        tool = await get_tool(
            mcp_server,
            "create_job",
        )

        job_input = CreateJobInput(
            id="JOB-001",
            title="Duplicate Job",
            description="Should fail",
            priority=Priority.HIGH,
        )

        result = await tool.fn(job_input)

        assert isinstance(result, ErrorResponse)

        assert result.error
        assert result.code
        assert result.suggestion

    # ============================================================
    # ASSIGN JOB
    # ============================================================

    @pytest.mark.asyncio
    async def test_assign_job_success(self, mcp_server):
        """Test assigning a job to a technician."""

        tool = await get_tool(
            mcp_server,
            "assign_job",
        )

        assign_input = AssignJobInput(
            job_id="JOB-001",
            technician_id="TECH-001",
        )

        result = await tool.fn(assign_input)

        assert result is not None

        assert result.job is not None

        assert result.job.id == "JOB-001"
        assert result.job.technician_id == "TECH-001"
        assert result.job.status == "assigned"

    @pytest.mark.asyncio
    async def test_assign_job_not_found(self, mcp_server):
        """Test assigning a non-existent job."""

        tool = await get_tool(
            mcp_server,
            "assign_job",
        )

        assign_input = AssignJobInput(
            job_id="JOB-999",
            technician_id="TECH-001",
        )

        result = await tool.fn(assign_input)

        assert isinstance(result, ErrorResponse)

        assert result.error
        assert result.code
        assert result.suggestion

    @pytest.mark.asyncio
    async def test_assign_job_unavailable_technician(
        self,
        mcp_server,
    ):
        """Test assigning a job to an unavailable technician."""

        tool = await get_tool(
            mcp_server,
            "assign_job",
        )

        assign_input = AssignJobInput(
            job_id="JOB-001",
            technician_id="TECH-003",
        )

        result = await tool.fn(assign_input)

        assert isinstance(result, ErrorResponse)

        assert result.error
        assert result.code
        assert result.suggestion

    # ============================================================
    # UPDATE JOB
    # ============================================================

    @pytest.mark.asyncio
    async def test_update_job_success(self, mcp_server):
        """Test updating a job."""

        tool = await get_tool(
            mcp_server,
            "update_job",
        )

        update_input = UpdateJobInput(
            job_id="JOB-001",
            title="Updated Title",
            status=JobStatus.ASSIGNED,
        )

        result = await tool.fn(update_input)

        assert result is not None

        assert result.job is not None

        assert result.job.id == "JOB-001"
        assert result.job.title == "Updated Title"
        assert result.job.status == JobStatus.ASSIGNED.value

    @pytest.mark.asyncio
    async def test_update_job_partial(self, mcp_server):
        """Test updating a job with partial data."""

        tool = await get_tool(
            mcp_server,
            "update_job",
        )

        update_input = UpdateJobInput(
            job_id="JOB-001",
            priority=Priority.LOW,
        )

        result = await tool.fn(update_input)

        assert result is not None

        assert result.job is not None

        assert result.job.id == "JOB-001"

        assert result.job.priority == Priority.LOW.value

    @pytest.mark.asyncio
    async def test_update_job_not_found(self, mcp_server):
        """Test updating a non-existent job."""

        tool = await get_tool(
            mcp_server,
            "update_job",
        )

        update_input = UpdateJobInput(
            job_id="JOB-999",
            title="Updated",
        )

        result = await tool.fn(update_input)

        assert isinstance(result, ErrorResponse)

        assert result.error
        assert result.code
        assert result.suggestion

    # ============================================================
    # DELETE JOB
    # ============================================================

    @pytest.mark.asyncio
    async def test_delete_job_success(self, mcp_server):
        """Test deleting a job."""

        tool = await get_tool(
            mcp_server,
            "delete_job",
        )

        delete_input = DeleteJobInput(
            job_id="JOB-001",
        )

        result = await tool.fn(delete_input)

        assert result is not None

        # Verify job was actually deleted.
        deleted_job = get_job("JOB-001")

        assert deleted_job is None

    @pytest.mark.asyncio
    async def test_delete_job_not_found(self, mcp_server):
        """Test deleting a non-existent job."""

        tool = await get_tool(
            mcp_server,
            "delete_job",
        )

        delete_input = DeleteJobInput(
            job_id="JOB-999",
        )

        result = await tool.fn(delete_input)

        assert isinstance(result, ErrorResponse)

        assert result.error
        assert result.code
        assert result.suggestion

    # ============================================================
    # IDEMPOTENCY
    # ============================================================

    @pytest.mark.asyncio
    async def test_idempotency_update_job(self, mcp_server):
        """Test idempotency when updating with the same values."""

        tool = await get_tool(
            mcp_server,
            "update_job",
        )

        original_job = get_job("JOB-001")

        assert original_job is not None

        original_title = original_job["title"]

        update_input = UpdateJobInput(
            job_id="JOB-001",
            title=original_title,
        )

        result1 = await tool.fn(update_input)

        result2 = await tool.fn(update_input)

        assert result1 is not None
        assert result2 is not None

        assert result1.job is not None
        assert result2.job is not None

        assert result1.job.id == "JOB-001"
        assert result2.job.id == "JOB-001"

        assert result1.job.title == original_title
        assert result2.job.title == original_title
