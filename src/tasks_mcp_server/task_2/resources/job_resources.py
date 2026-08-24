from typing import Union

from src.tasks_mcp_server.task_2.data import data as D
from src.tasks_mcp_server.task_2.schemas.error_schemas import ErrorResponse


def register_job_resources(mcp):

    @mcp.resource(
        "task-1://list_of_jobs",
        mime_type="application/json",
    )
    def all_jobs() -> Union[list, ErrorResponse]:
        """Give list of all jobs."""

        try:
            return D.jobs

        except AttributeError:
            return ErrorResponse(
                error="Unable to retrieve all jobs: job data is unavailable",
                code="JOB_DATA_UNAVAILABLE",
                suggestion=(
                    "Verify that the job data source is available "
                    "and try again."
                ),
            )

        except Exception:
            return ErrorResponse(
                error=(
                    "Unable to retrieve all jobs: "
                    "an unexpected error occurred"
                ),
                code="INTERNAL_ERROR",
                suggestion=(
                    "Verify the job data and try again."
                ),
            )


    @mcp.resource(
        "task-1://list_of_open_jobs",
        mime_type="application/json",
    )
    def open_jobs() -> Union[list, ErrorResponse]:
        """Give list of all open jobs."""

        try:
            return [
                job
                for job in D.jobs
                if job["status"] == "open"
            ]

        except KeyError:
            return ErrorResponse(
                error=(
                    "Unable to retrieve open jobs: "
                    "required job field is missing"
                ),
                code="JOB_DATA_FIELD_MISSING",
                suggestion=(
                    "Verify that all job data contains "
                    "the required status field."
                ),
            )

        except TypeError:
            return ErrorResponse(
                error=(
                    "Unable to retrieve open jobs: "
                    "invalid job data"
                ),
                code="INVALID_JOB_DATA",
                suggestion=(
                    "Verify that the job data has the expected "
                    "dictionary structure."
                ),
            )

        except Exception:
            return ErrorResponse(
                error=(
                    "Unable to retrieve open jobs: "
                    "an unexpected error occurred"
                ),
                code="INTERNAL_ERROR",
                suggestion=(
                    "Verify the job data and try again."
                ),
            )