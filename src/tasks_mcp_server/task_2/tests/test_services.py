import pytest
from src.tasks_mcp_server.task_2.data import data as D
from src.tasks_mcp_server.task_2.services.validation_services import get_job, get_technician


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


class TestValidationServices:
    """Test validation services."""

    @pytest.mark.parametrize(
        "job_id, expected_id, expected_title",
        [
            ("JOB-001", "JOB-001", "Job 1"),
            ("JOB-999", None, None),
            ("JOB-BAD", "JOB-BAD", None),
        ],
        ids=[
            "job_found",
            "job_not_found",
            "invalid_job_data",
        ],
    )
    def test_get_job(
        self,
        job_id,
        expected_id,
        expected_title,
    ):
        """Test getting existing, missing, and invalid jobs."""

        if job_id == "JOB-BAD":
            D.jobs.append({"id": "JOB-BAD"})

        job = get_job(job_id)

        if expected_id is None:
            assert job is None
        else:
            assert job is not None
            assert job["id"] == expected_id

            if expected_title is not None:
                assert job["title"] == expected_title




    @pytest.mark.parametrize(
        "technician_id, expected_id, expected_name",
        [
            ("TECH-001", "TECH-001", "Tech 1"),
            ("TECH-999", None, None),
            ("TECH-BAD", "TECH-BAD", None),
        ],
        ids=[
            "technician_found",
            "technician_not_found",
            "invalid_technician_data",
        ],
    )
    def test_get_technician(
        self,
        technician_id,
        expected_id,
        expected_name,
    ):
        """Test getting existing, missing, and invalid technicians."""

        if technician_id == "TECH-BAD":
            D.technicians.append({"id": "TECH-BAD"})

        tech = get_technician(technician_id)

        if expected_id is None:
            assert tech is None
        else:
            assert tech is not None
            assert tech["id"] == expected_id

            if expected_name is not None:
                assert tech["name"] == expected_name
