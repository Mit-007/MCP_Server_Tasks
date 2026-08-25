from src.tasks_mcp_server.task_1.data import data as D


def register_job_resources(mcp):

    @mcp.resource("jobs://all", mime_type="application/json")
    def all_jobs():
        """give list of all jobs."""
        try:
            return D.jobs

        except AttributeError as exc:
            return (
                f"Unable to retrieve all jobs: job data is unavailable ({exc}).\n"
                f"Suggestion: verify that the job data source is available and try again."
            )

        except Exception as exc:
            return (
                f"Unable to retrieve all jobs: an unexpected error occurred ({exc}).\n"
                f"Suggestion: verify the job data and try again."
            )

    @mcp.resource("jobs://open", mime_type="application/json")
    def open_jobs():
        """give list of all Open jobs."""
        try:
            return [
                job
                for job in D.jobs
                if job["status"] == "open"
            ]

        except KeyError as exc:
            return (
                f"Unable to retrieve open jobs: required job field is missing ({exc}).\n"
                f"Suggestion: verify that all job data contains the required status field."
            )

        except TypeError as exc:
            return (
                f"Unable to retrieve open jobs: invalid job data ({exc}).\n"
                f"Suggestion: verify that the job data has the expected dictionary structure."
            )

        except Exception as exc:
            return (
                f"Unable to retrieve open jobs: an unexpected error occurred ({exc}).\n"
                f"Suggestion: verify the job data and try again."
            )