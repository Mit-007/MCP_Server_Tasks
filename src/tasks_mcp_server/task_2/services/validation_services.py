from src.tasks_mcp_server.task_2.data import data as D
from src.tasks_mcp_server.task_2.schemas.error_schemas import ErrorResponse


def get_job(job_id: str):
    """Find job for given job_id."""

    try:
        existing_job = next(
            (
                job
                for job in D.jobs
                if job["id"] == job_id
            ),
            None,
        )

        return existing_job

    except KeyError as exc:
        return ErrorResponse(
            error=(
                f"Unable to find Job {job_id}: "
                f"required job field is missing ({exc})"
            ),
            code="JOB_DATA_FIELD_MISSING",
            suggestion=(
                "Verify that the job data contains all required fields."
            ),
        )

    except TypeError as exc:
        return ErrorResponse(
            error=(
                f"Unable to find Job {job_id}: "
                f"invalid job data ({exc})"
            ),
            code="INVALID_JOB_DATA",
            suggestion=(
                "Verify that the job data has the expected "
                "dictionary structure."
            ),
        )

    except Exception:
        return ErrorResponse(
            error=f"Unable to find Job {job_id}: an unexpected error occurred",
            code="INTERNAL_ERROR",
            suggestion=(
                "Verify the job ID and job data, then try again."
            ),
        )


def get_technician(technician_id: str):
    """Find a technician for given technician_id."""

    try:
        existing_technician = next(
            (
                technician
                for technician in D.technicians
                if technician["id"] == technician_id
            ),
            None,
        )

        return existing_technician

    except KeyError as exc:
        return ErrorResponse(
            error=(
                f"Unable to find Technician {technician_id}: "
                f"required technician field is missing ({exc})"
            ),
            code="TECHNICIAN_DATA_FIELD_MISSING",
            suggestion=(
                "Verify that the technician data contains "
                "all required fields."
            ),
        )

    except TypeError as exc:
        return ErrorResponse(
            error=(
                f"Unable to find Technician {technician_id}: "
                f"invalid technician data ({exc})"
            ),
            code="INVALID_TECHNICIAN_DATA",
            suggestion=(
                "Verify that the technician data has the expected "
                "dictionary structure."
            ),
        )

    except Exception:
        return ErrorResponse(
            error=(
                f"Unable to find Technician {technician_id}: "
                "an unexpected error occurred"
            ),
            code="INTERNAL_ERROR",
            suggestion=(
                "Verify the technician ID and technician data, "
                "then try again."
            ),
        )