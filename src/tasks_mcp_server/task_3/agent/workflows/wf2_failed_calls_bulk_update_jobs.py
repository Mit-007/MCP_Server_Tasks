from src.tasks_mcp_server.task_3.agent.services.llm import llm
from src.tasks_mcp_server.task_3.agent.core.logger import logger
from src.tasks_mcp_server.task_3.agent.schemas.workflow_schemas import (
    FailedCallJobMatchingOutput,
)
import json
from langchain.tools import tool

@tool
async def match_failed_calls_jobs_update_workflow(
    tools_by_name: dict = None,
):
    """
    Workflow:

    1. Fetch all failed call logs.
    2. Ask LLM to extract job IDs from the notes of failed calls.
    3. Fetch all open jobs.
    4. Check which open jobs are present in the extracted job ID list.
    5. Update those jobs from open -> cancelled.
    """

    # ============================================================
    # STEP 1: Fetch all failed calls
    # ============================================================

    list_failed_calls_tool = tools_by_name["call_log_server_list_calls_by_status"]

    logger.info("Fetching all failed calls")

    cursor = None

    failed_call_logs = []
    
    while(True):
        failed_calls_result = await list_failed_calls_tool.ainvoke(
            {
                "data": {
                    "status": "failed",
                    "limit": 10,
                    "cursor": cursor,
                }
            }
        )
        text = failed_calls_result[0]["text"]
        
        # 2. Convert JSON string → Python dict
        text_json = json.loads(text)
    
        # 3. Fetch pagination information
        has_more = text_json["has_more"]
        next_cursor = text_json["next_cursor"]
        data = text_json["data"]
        
        print("current_data_size:", len(data))
        print("has_more:", has_more)
        print("next_cursor:", next_cursor)

        failed_call_logs.extend(data)
        print("all_data_list_size:", len(failed_call_logs))

        if has_more == False :
            break

        cursor = next_cursor

    logger.info(
        f"Failed calls logs result: {failed_calls_result}"
    )

    # ============================================================
    # STEP 2: Extract job IDs from failed call notes
    # ============================================================

    prompt = f"""
You are executing a failed-call job cancellation workflow.

Your task is ONLY to identify job IDs that are mentioned
inside the notes of FAILED call logs.

Below are the failed call logs list:

{failed_call_logs}

IMPORTANT RULES:

1. Look ONLY at the notes field of each call.
2. Find notes containing a job reference such as:

   "Related job_id: JOB-011"

3. Extract only the job ID.

Example:

Note:
"Related job_id: JOB-011"

Output:
"JOB-011"

4. Ignore notes that do not contain a job ID.

5. Do not create or guess any job IDs.

6. Do not use the transcript to determine the job ID.
   The job ID must come from the call's notes.

7. Return every unique job ID found in the failed calls.

If at least one job ID is found:
- next = true

If no job ID is found:
- next = false
- cancelled_job_ids = []

Return the result using the required structured output.
"""

    structured_llm = llm.with_structured_output(
        FailedCallJobMatchingOutput
    )

    response = structured_llm.invoke(prompt)

    logger.info(
        f"FAILED CALL JOB MATCHING RESPONSE: {response}"
    )

    if not response.next:
        logger.info(
            "No job IDs found in failed call notes."
        )

        return {
            "cancelled_job_ids": [],
            "updated_jobs": [],
        }

    cancelled_job_ids = response.cancelled_job_ids

    logger.info(
        f"Job IDs extracted from failed calls: "
        f"{cancelled_job_ids}"
    )

     # ============================================================
    # STEP 3: Fetch all open jobs
    # ============================================================

    list_open_jobs_tool = tools_by_name["job_server_open_jobs"]

    logger.info("Fetching all open jobs")

    cursor = None
    
    open_jobs_list = []

    while(True):
        open_jobs_result = await list_open_jobs_tool.ainvoke(
            {
                "data": {
                    "limit": 100,
                    "cursor": cursor,
                }
            }
        )
        text = open_jobs_result[0]["text"]
        
        # 2. Convert JSON string → Python dict
        text_json = json.loads(text)
    
        # 3. Fetch pagination information
        has_more = text_json["has_more"]
        next_cursor = text_json["next_cursor"]
        data = text_json["data"]
        
        print("current_data_size:", len(data))
        print("has_more:", has_more)
        print("next_cursor:", next_cursor)

        open_jobs_list.extend(data)
        print("all_data_list_size:", len(open_jobs_list))

        if has_more == False :
            break

        cursor = next_cursor

    # ============================================================
    # STEP 4: Loop through open jobs
    # ============================================================

    updated_jobs = []

    for job in open_jobs_list:
        print("------------------------------------------------------------")
        print(job)
        print("------------------------------------------------------------")

        job_id = job["id"]

        logger.info(
            f"Checking open job: {job_id}"
        )

        # --------------------------------------------------------
        # Check whether this job was referenced by a failed call
        # --------------------------------------------------------

        if job_id not in cancelled_job_ids:
            continue

        logger.info(
            f"Job {job_id} found in failed call references. "
            f"Cancelling job."
        )

        # ========================================================
        # STEP 5: Update job status
        # ========================================================

        update_job_tool = tools_by_name["job_server_update_job"]

        update_result = await update_job_tool.ainvoke(
            {
                "data": {
                    "job_id": job_id,
                    "status": "cancelled",
                }
            }
        )

        logger.info(
            f"Job {job_id} cancelled successfully: "
            f"{update_result}"
        )

        updated_jobs.append(
            {
                "job_id": job_id,
                "result": update_result,
            }
        )

    # ============================================================
    # Workflow Complete
    # ============================================================

    return {
        "cancelled_job_ids": cancelled_job_ids,
        "updated_jobs": updated_jobs,
    }

