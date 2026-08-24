from src.tasks_mcp_server.task_1.data import data as D


def get_job(job_id: str):
    """find job for given job_id"""
    try:
        existing_job = next(
            (job for job in D.jobs if job["id"] == job_id),
            None,
        )

        return existing_job

    except KeyError as exc:
        raise KeyError(
            f"Unable to find Job {job_id}: required job field is missing ({exc}).\n"
            f"Suggestion: verify that the job data contains all required fields."
        ) from exc

    except TypeError as exc:
        raise TypeError(
            f"Unable to find Job {job_id}: invalid job data ({exc}).\n"
            f"Suggestion: verify that the job data has the expected dictionary structure."
        ) from exc

    except Exception as exc:
        raise RuntimeError(
            f"Unable to find Job {job_id}: an unexpected error occurred ({exc}).\n"
            f"Suggestion: verify the job ID and job data, then try again."
        ) from exc


def get_technician(technician_id: str):
    """find a technician for given technician_id"""
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
        raise KeyError(
            f"Unable to find Technician {technician_id}: required technician field is missing ({exc}).\n"
            f"Suggestion: verify that the technician data contains all required fields."
        ) from exc

    except TypeError as exc:
        raise TypeError(
            f"Unable to find Technician {technician_id}: invalid technician data ({exc}).\n"
            f"Suggestion: verify that the technician data has the expected dictionary structure."
        ) from exc

    except Exception as exc:
        raise RuntimeError(
            f"Unable to find Technician {technician_id}: an unexpected error occurred ({exc}).\n"
            f"Suggestion: verify the technician ID and technician data, then try again."
        ) from exc