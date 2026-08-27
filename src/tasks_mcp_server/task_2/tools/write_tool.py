from typing import Union
from src.tasks_mcp_server.task_2.data import data as D
from src.tasks_mcp_server.task_2.schemas.tool_output_schemas import JobMutationResponse
from src.tasks_mcp_server.task_2.schemas.error_schemas import ErrorResponse
from src.tasks_mcp_server.task_2.schemas.tool_input_schemas import (CreateJobInput,AssignJobInput,DeleteJobInput,UpdateJobInput,)
from src.tasks_mcp_server.task_2.services.validation_services import (get_job,get_technician,)
from src.tasks_mcp_server.task_2.core.logger import logger

def register_write_tool(mcp):

    @mcp.tool(
        annotations={
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": False,
        }
    )
    async def create_job(
        data: CreateJobInput,
    ) -> Union[JobMutationResponse, ErrorResponse]:
        """Create a new job in the system."""

        try:
            # Check if job with same ID already exists
            existing_job = get_job(data.id)

            if existing_job is not None:
                return ErrorResponse(
                    error=f"Job with ID {data.id} already exists",
                    code="JOB_ALREADY_EXISTS",
                    suggestion=(
                        "Use a different job ID, or call update_job "
                        "if you meant to modify the existing job."
                    ),
                )

            # Create new job
            new_job = {
                "id": data.id,
                "title": data.title,
                "status": "open",
                "description": data.description,
                "priority": data.priority,
                "technician_id": None,
            }

            D.jobs.append(new_job)

            return JobMutationResponse(
                success=True,
                message=f"Job {data.id} created successfully",
                job=new_job,
            )

        except Exception as e:
            logger.error(f"Unexpected error in list_jobs: {str(e)}", exc_info=True)
            return ErrorResponse(
                error="Failed to create job",
                code="INTERNAL_ERROR",
                suggestion="Please try again later.",
            )


    @mcp.tool(
        annotations={
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": False,
        }
    )
    async def assign_job(
        data: AssignJobInput,
    ) -> Union[JobMutationResponse, ErrorResponse]:
        """Assign a job to an available technician."""

        try:
            job = get_job(data.job_id)

            if job is None:
                return ErrorResponse(
                    error=f"Job {data.job_id} not found",
                    code="JOB_NOT_FOUND",
                    suggestion=(
                        "Call list_jobs to see valid job IDs "
                        "and try again."
                    ),
                )

            if job["status"] != "open":
                return ErrorResponse(
                    error=(
                        f"Job {data.job_id} is not open for assignment "
                        f"(current status: {job['status']})"
                    ),
                    code="JOB_NOT_OPEN",
                    suggestion=(
                        "Choose a different job that is open, "
                        "or call update_job to reset its status first."
                    ),
                )

            technician = get_technician(data.technician_id)

            if technician is None:
                return ErrorResponse(
                    error=f"Technician {data.technician_id} not found",
                    code="TECHNICIAN_NOT_FOUND",
                    suggestion=(
                        "Call list_technicians to see valid technician IDs "
                        "and try again."
                    ),
                )

            if technician["available"] is not True:
                return ErrorResponse(
                    error=(
                        f"Technician {data.technician_id} is not available"
                    ),
                    code="TECHNICIAN_UNAVAILABLE",
                    suggestion=(
                        "Call get_available_technicians to find an "
                        "available technician and retry."
                    ),
                )

            job["status"] = "assigned"
            job["technician_id"] = data.technician_id

            technician["available"] = False

            return JobMutationResponse(
                success=True,
                message=(
                    f"Job {data.job_id} assigned to "
                    f"{data.technician_id} successfully"
                ),
                job=job,
            )

        except Exception:
            return ErrorResponse(
                error="Failed to assign job",
                code="INTERNAL_ERROR",
                suggestion="Please try again later.",
            )


    @mcp.tool(
        annotations={
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        }
    )
    async def update_job(
        data: UpdateJobInput,
    ) -> Union[JobMutationResponse, ErrorResponse]:
        """Update one or more fields of an existing job."""

        try:
            job = get_job(data.job_id)

            if job is None:
                return ErrorResponse(
                    error=f"Job {data.job_id} not found",
                    code="JOB_NOT_FOUND",
                    suggestion=(
                        "Call list_jobs to see valid job IDs "
                        "and try again."
                    ),
                )

            if data.title is not None:
                job["title"] = data.title

            if data.description is not None:
                job["description"] = data.description

            if data.priority is not None:
                job["priority"] = data.priority

            if data.status is not None:
                job["status"] = data.status

            if data.technician_id is not None:
                job["technician_id"] = data.technician_id

            return JobMutationResponse(
                success=True,
                message=f"Job {data.job_id} updated successfully",
                job=job,
            )

        except Exception:
            return ErrorResponse(
                error="Failed to update job",
                code="INTERNAL_ERROR",
                suggestion="Please try again later.",
            )


    @mcp.tool(
        annotations={
            "readOnlyHint": False,
            "destructiveHint": True,
            "idempotentHint": False,
            "openWorldHint": False,
        }
    )
    async def delete_job(
        data: DeleteJobInput,
    ) -> Union[JobMutationResponse, ErrorResponse]:
        """Delete a job from the system."""

        try:
            job_index = next(
                (i for i, job in enumerate(D.jobs) if job["id"] == data.job_id),
                None
            )
            
            if job_index is None:
                return ErrorResponse(
                    error=f"Job {data.job_id} not found",
                    code="JOB_NOT_FOUND",
                    suggestion="Call list_jobs to see valid job IDs and try again.",
                )
            
            job = D.jobs[job_index]
            
            # Restore technician availability
            if job["technician_id"] is not None:
                technician = get_technician(job["technician_id"])
                if technician is not None:
                    technician["available"] = True

            D.jobs.pop(job_index)
            
            return JobMutationResponse(
                success=True,
                message=f"Job {data.job_id} deleted successfully",
                job=job,
            )

        except Exception:
            return ErrorResponse(
                error="Failed to delete job",
                code="INTERNAL_ERROR",
                suggestion="Please try again later.",
            )