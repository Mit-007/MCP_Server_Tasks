from src.tasks_mcp_server.task_1.data import data as D
from src.tasks_mcp_server.task_1.schemas.tool_output_schemas import JobMutationResponse
from src.tasks_mcp_server.task_1.schemas.tool_input_schemas import CreateJobInput,AssignJobInput,DeleteJobInput,UpdateJobInput
from src.tasks_mcp_server.task_1.services.validation_services import get_job ,get_technician


def register_write_tool(mcp):

    @mcp.tool()
    async def create_job(data : CreateJobInput) -> JobMutationResponse:
        """ Create a new job in the system."""
        try:
            existing_job = get_job(data.id)
            if existing_job is not None:
                return JobMutationResponse(
                    success=False,
                    message=f"Job with ID {data.id} already exists. Use a different job ID, or call update_job if you meant to modify the existing job.",
                    job=None,
                )

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
            return JobMutationResponse(
                success=False,
                message=f"Unexpected error while creating job {data.id}: {str(e)}. Verify the input fields are valid and retry; if the problem persists, contact support.",
                job=None,
            )


    @mcp.tool()
    async def assign_job(data : AssignJobInput) -> JobMutationResponse:
        """  Assign a job to an available technician. """
        try:
            job = get_job(data.job_id)

            if job is None:
                return JobMutationResponse(
                    success=False,
                    message=f"Job {data.job_id} not found. Call list_jobs to see valid job IDs and try again.",
                    job=None,
                )

            if job["status"] != "open":
                return JobMutationResponse(
                    success=False,
                    message=f"Job {data.job_id} is not open for assignment (current status: {job['status']}). Choose a different job that is open, or call update_job to reset its status first.",
                    job=job,
                )

            technician = get_technician(data.technician_id)

            if technician is None:
                return JobMutationResponse(
                    success=False,
                    message=f"Technician {data.technician_id} not found. Call list_technicians to see valid technician IDs and try again.",
                    job=job,
                )

            if technician["available"] is not True:
                return JobMutationResponse(
                    success=False,
                    message=f"Technician {data.technician_id} is not available. Call get_available_technicians to find an available technician and retry.",
                    job=job,
                )

            job["status"] = "assigned"
            job["technician_id"] = data.technician_id

            technician["available"] = False

            return JobMutationResponse(
                success=True,
                message=f"Job {data.job_id} assigned to {data.technician_id} successfully",
                job=job,
            )
        except Exception as e:
            return JobMutationResponse(
                success=False,
                message=f"Unexpected error while assigning job {data.job_id}: {str(e)}. Verify the job and technician IDs are correct and retry; if the problem persists, contact support.",
                job=None,
            )


    @mcp.tool()
    async def update_job(data : UpdateJobInput) -> JobMutationResponse:
        """ Update one or more fields of an existing job."""
        try:
            job = get_job(data.job_id)

            if job is None:
                return JobMutationResponse(
                    success=False,
                    message=f"Job {data.job_id} not found. Call list_jobs to see valid job IDs and try again.",
                    job=None,
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
        except Exception as e:
            return JobMutationResponse(
                success=False,
                message=f"Unexpected error while updating job {data.job_id}: {str(e)}. Verify the fields you are updating are valid and retry; if the problem persists, contact support.",
                job=None,
            )


    @mcp.tool()
    async def delete_job(data : DeleteJobInput) -> JobMutationResponse:
        """Delete a job from the system."""
        try:
            for job in D.jobs:
                if job["id"] == data.job_id:
                    if job["technician_id"] is not None:
                        technician = get_technician(job["technician_id"])

                        if technician is not None:
                            technician["available"] = True

                    D.jobs.remove(job)

                    return JobMutationResponse(
                            success=True,
                            message=f"Job {data.job_id} deleted successfully",
                            job=job,
                    )

            return JobMutationResponse(
                success=False,
                message=f"Job {data.job_id} not found. Call list_jobs to see valid job IDs and try again.",
                job=None,
            )
        except Exception as e:
            return JobMutationResponse(
                success=False,
                message=f"Unexpected error while deleting job {data.job_id}: {str(e)}. Verify the job ID is correct and retry; if the problem persists, contact support.",
                job=None,
            )