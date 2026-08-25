from typing import Union
import json
from src.tasks_mcp_server.task_2.data import data as D
from src.tasks_mcp_server.task_2.schemas.error_schemas import ErrorResponse


def register_job_resources(mcp):

    @mcp.resource(
        "jobs://all",
        mime_type="application/json",
    )
    async def all_jobs() -> str:
        """Give list of all jobs."""

        try:
            return json.dumps(D.jobs)

        except AttributeError:
            error = ErrorResponse(
                error="Unable to retrieve all jobs: job data is unavailable",
                code="JOB_DATA_UNAVAILABLE",
                suggestion=(
                    "Verify that the job data source is available "
                    "and try again."
                ),
            )
            return json.dumps(error.model_dump())

        except Exception:
            error = ErrorResponse(
                error=(
                    "Unable to retrieve all jobs: "
                    "an unexpected error occurred"
                ),
                code="INTERNAL_ERROR",
                suggestion=(
                    "Verify the job data and try again."
                ),
            )
            return json.dumps(error.model_dump())


    @mcp.resource(
        "jobs://open",
        mime_type="application/json",
    )
    async def open_jobs() -> str:
        """Give list of all open jobs."""

        try:
            open_jobs_list = [
                job
                for job in D.jobs
                if job["status"] == "open"
            ]
            return json.dumps(open_jobs_list)

        except KeyError:
            error = ErrorResponse(
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
            return json.dumps(error.model_dump())

        except TypeError:
            error = ErrorResponse(
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
            return json.dumps(error.model_dump())

        except Exception:
            error = ErrorResponse(
                error=(
                    "Unable to retrieve open jobs: "
                    "an unexpected error occurred"
                ),
                code="INTERNAL_ERROR",
                suggestion=(
                    "Verify the job data and try again."
                ),
            )
            return json.dumps(error.model_dump())