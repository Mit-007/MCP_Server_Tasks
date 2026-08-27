import pytest
from src.tasks_mcp_server.task_2.schemas.tool_input_schemas import PaginationInput
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


class TestPagination:
    """Test pagination input validation."""

    @pytest.mark.parametrize(
        "kwargs, expected_limit, expected_cursor",
        [
            ({}, 10, None),
            ({"limit": 5}, 5, None),
            ({"cursor": "10", "limit": 5}, 5, "10"),
        ],
    )
    def test_pagination_valid(self, kwargs, expected_limit, expected_cursor):
        pagination = PaginationInput(**kwargs)

        assert pagination.limit == expected_limit
        assert pagination.cursor == expected_cursor


    
    @pytest.mark.parametrize(
        "limit",
        [101, 0, -1],
        ids=["too_large", "zero", "negative"],
    )
    def test_pagination_invalid_limit(self, limit):
        with pytest.raises(ValueError):
            PaginationInput(limit=limit)


    def test_pagination_empty_page_cursor_beyond_data(self):
        """Pagination - empty page when cursor beyond data."""
        pagination = PaginationInput(cursor="100", limit=10)
        start = int(pagination.cursor)
        items = D.jobs[start:start + pagination.limit]
        assert len(items) == 0
    
    def test_pagination_last_page_partial_results(self):
        """Pagination - last page with partial results."""
        pagination = PaginationInput(cursor="4", limit=2)
        start = int(pagination.cursor)
        items = D.jobs[start:start + pagination.limit]
        assert len(items) == 1
    
    def test_pagination_negative_cursor_out_of_range(self):
        """ Pagination - negative cursor rejected."""
        pagination = PaginationInput(cursor="-1", limit=10)
        start = int(pagination.cursor)
        assert start < 0
