from src.tasks_mcp_server.task_1.data import data as D
from src.tasks_mcp_server.task_1.schemas import tool_output_schemas as TS


def register_read_tools(mcp):

    @mcp.tool()
    async def list_jobs() -> TS.JobsOutput:
        """list of all jobs"""
        try:
            return TS.JobsOutput(jobs=D.jobs)

        except Exception as e:
            raise RuntimeError(
                f"Failed to list jobs: {str(e)}.\n"
                f"Suggestion: retry the request; if the problem persists, check resources jobs://all."
            )

    @mcp.tool()
    async def list_technicians() -> TS.TechniciansOutput:
        """list of all technicians"""
        try:
            return TS.TechniciansOutput(technicians=D.technicians)

        except Exception as e:
            raise RuntimeError(
                f"Failed to list technicians: {str(e)}.\n"
                f"Suggestion: retry the request; if the problem persists, check the technician data."
            )

    @mcp.tool()
    async def get_available_technicians() -> TS.TechniciansOutput:
        """list of all available technicians"""
        try:
            available = [
                technician
                for technician in D.technicians
                if technician["available"]
            ]

            return TS.TechniciansOutput(technicians=available)

        except Exception as e:
            raise RuntimeError(
                f"Failed to get available technicians: {str(e)}.\n"
                f"Suggestion: retry the request, or call list_technicians to check technician data."
            )

    @mcp.tool()
    async def open_jobs() -> TS.JobsOutput:
        """list of all open jobs"""
        try:
            open_jobs = [
                job
                for job in D.jobs
                if job["status"] == "open"
            ]

            return TS.JobsOutput(jobs=open_jobs)

        except Exception as e:
            raise RuntimeError(
                f"Failed to get open jobs: {str(e)}.\n"
                f"Suggestion: retry the request, or call list_jobs to check job data."
            )