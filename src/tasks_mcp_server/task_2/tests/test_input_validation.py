import pytest
from src.tasks_mcp_server.task_2.schemas.tool_input_schemas import CreateJobInput, AssignJobInput, UpdateJobInput, DeleteJobInput, Priority


class TestInputSchemas:
    """Test input schema validation."""
    
    def test_create_job_input_valid(self):
        """Test CreateJobInput validation."""
        job_input = CreateJobInput(
            id="JOB-123",
            title="Test Job",
            description="Test Description",
            priority=Priority.HIGH
        )
        assert job_input.id == "JOB-123"
        assert job_input.title == "Test Job"
    
    def test_create_job_input_invalid_id_too_short(self):
        """Test CreateJobInput with ID too short."""
        with pytest.raises(ValueError):
            CreateJobInput(
                id="JB",
                title="Test",
                description="Desc",
                priority=Priority.HIGH
            )
    
    def test_create_job_input_invalid_priority(self):
        """Test CreateJobInput with invalid priority."""
        with pytest.raises(ValueError):
            CreateJobInput(
                id="JOB-123",
                title="Test",
                description="Desc",
                priority="invalid"
            )
    
    def test_assign_job_input_valid(self):
        """Test AssignJobInput validation."""
        assign_input = AssignJobInput(
            job_id="JOB-123",
            technician_id="TECH-001"
        )
        assert assign_input.job_id == "JOB-123"
    
    def test_update_job_input_valid(self):
        """Test UpdateJobInput validation."""
        update_input = UpdateJobInput(
            job_id="JOB-123",
            title="Updated"
        )
        assert update_input.job_id == "JOB-123"
        assert update_input.title == "Updated"
    
    def test_delete_job_input_valid(self):
        """Test DeleteJobInput validation."""
        delete_input = DeleteJobInput(job_id="JOB-123")
        assert delete_input.job_id == "JOB-123"