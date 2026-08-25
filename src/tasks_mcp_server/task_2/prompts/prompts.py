from typing import Union
import json

from src.tasks_mcp_server.task_2.data import data as D
from src.tasks_mcp_server.task_2.schemas.error_schemas import ErrorResponse
from src.tasks_mcp_server.task_2.services.validation_services import get_job


def register_prompts(mcp):

    @mcp.prompt()
    async def triage_job(
        job_id: str,
    ) -> str:
        """Analyze a job and provide a triage assessment.

        Retrieves the job using the provided job ID and generates a prompt
        for analyzing the job's problem, severity, required skills, urgency,
        recommended action, and whether immediate technician assignment
        is recommended.
        """

        try:
            job = get_job(job_id)

            if job is None:
                error = ErrorResponse(
                    error=f"Job {job_id} was not found",
                    code="JOB_NOT_FOUND",
                    suggestion=(
                        "Provide a valid existing job ID. "
                        "Call list_jobs to see available jobs."
                    ),
                )
                return json.dumps(error.model_dump())

            return f"""You are an expert job triage assistant for a field service operations team.

Analyze the following job and produce a structured triage assessment. Base your analysis strictly on the information provided below — do not assume facts that are not stated.

JOB DETAILS
- Job ID: {job["id"]}
- Title: {job["title"]}
- Description: {job["description"]}
- Priority: {job["priority"]}
- Status: {job["status"]}

Provide your assessment in the following structured format:

1. Problem Summary
   A concise 1-2 sentence restatement of the core issue.

2. Severity (Low / Medium / High / Critical)
   Your assessed severity level, with a one-sentence justification.

3. Required Skills
   A bullet list of the specific technical skills, certifications, or expertise needed to resolve this job.

4. Recommended Action
   The concrete next step(s) that should be taken, in priority order.

5. Urgency (Can Wait / Same-Day / Immediate)
   How quickly this job needs to be addressed, with a brief justification based on severity and stated priority.

6. Immediate Assignment Recommendation (Yes / No)
   State clearly whether a technician should be assigned right now, and explain why in one sentence.

Be concise and specific. If the description lacks enough detail to confidently assess any section, say so explicitly rather than guessing.
"""

        except KeyError:
            error = ErrorResponse(
                error=(
                    f"Unable to triage Job {job_id}: "
                    "required job field is missing"
                ),
                code="JOB_DATA_FIELD_MISSING",
                suggestion=(
                    "Verify that the job data contains all required fields."
                ),
            )
            return json.dumps(error.model_dump())

        except TypeError:
            error = ErrorResponse(
                error=(
                    f"Unable to triage Job {job_id}: "
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
                    f"Unable to triage Job {job_id}: "
                    "an unexpected error occurred"
                ),
                code="INTERNAL_ERROR",
                suggestion=(
                    "Verify the job ID and job data, then try again."
                ),
            )
            return json.dumps(error.model_dump())


    @mcp.prompt()
    async def assign_suggestion(
        job_id: str,
    ) -> str:
        """Recommend the best available technician for a job.

        Retrieves the job using the provided job ID and generates a prompt
        that evaluates available technicians based on their skills,
        compatibility with the job requirements, availability, and job
        priority.
        """

        try:
            job = get_job(job_id)

            if job is None:
                error = ErrorResponse(
                    error=f"Job {job_id} was not found",
                    code="JOB_NOT_FOUND",
                    suggestion=(
                        "Provide a valid existing job ID. "
                        "Call list_jobs to see available jobs."
                    ),
                )
                return json.dumps(error.model_dump())

            available_technicians = [
                technician
                for technician in D.technicians
                if technician["available"] is True
            ]

            if not available_technicians:
                error = ErrorResponse(
                    error=(
                        f"No available technicians were found for "
                        f"Job {job['id']}."
                    ),
                    code="NO_AVAILABLE_TECHNICIANS",
                    suggestion=(
                        "Wait for a technician to become available "
                        "and retry the recommendation."
                    ),
                )
                return json.dumps(error.model_dump())

            technician_list = "\n".join(
                f"- ID: {t['id']} | Name: {t['name']} | "
                f"Skills: {t.get('skills', 'N/A')} | "
                f"Availability: {t.get('available')}"
                for t in available_technicians
            )

            return f"""You are an expert technician assignment assistant for a field service operations team.

Evaluate the available technicians below and recommend the single best fit for this job. Base your evaluation strictly on the information provided — do not assume facts that are not stated.

JOB DETAILS
- Job ID: {job["id"]}
- Title: {job["title"]}
- Description: {job["description"]}
- Priority: {job["priority"]}

AVAILABLE TECHNICIANS
{technician_list}

Evaluate each candidate against:
1. Skill match — how well their listed skills align with the job's requirements
2. Job requirements — technical demands implied by the description
3. Availability — confirm they are currently available
4. Job priority — how urgency should influence the selection (e.g. favor stronger skill match for high-priority jobs)

Return your recommendation in the following structured format:

1. Recommended Technician ID
2. Technician Name
3. Skill Match
   A brief explanation of how their skills align with this job's needs.
4. Reason for Selection
   Why this technician was chosen over the other candidates.
5. Confidence Level (Low / Medium / High)
   With a one-sentence justification.

If no candidate is a strong fit, say so explicitly and explain what skill or attribute is missing rather than forcing a recommendation.

Do not assign the technician. Only provide a recommendation.
"""

        except KeyError:
            error = ErrorResponse(
                error=(
                    f"Unable to generate assignment suggestion for "
                    f"Job {job_id}: required data field is missing"
                ),
                code="JOB_DATA_FIELD_MISSING",
                suggestion=(
                    "Verify that the job data contains all required fields."
                ),
            )
            return json.dumps(error.model_dump())

        except TypeError:
            error = ErrorResponse(
                error=(
                    f"Unable to generate assignment suggestion for "
                    f"Job {job_id}: invalid data"
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
                    f"Unable to generate assignment suggestion for "
                    f"Job {job_id}: an unexpected error occurred"
                ),
                code="INTERNAL_ERROR",
                suggestion=(
                    "Verify the job ID and job data, then try again."
                ),
            )
            return json.dumps(error.model_dump())