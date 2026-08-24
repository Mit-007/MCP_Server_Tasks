from src.tasks_mcp_server.task_3.agent.services.llm import llm
from src.tasks_mcp_server.task_3.agent.core.logger import logger
from src.tasks_mcp_server.task_3.agent.schemas.workflow_schemas import (
    FollowUpJobCreationOutput,
)
import json
import uuid
from langchain.tools import tool

@tool
async def create_follow_up_jobs_workflow(
    tools_by_name: dict = None,
):
    """
    Workflow: Create Follow-up Jobs from Call Outcomes

    1. Fetch all calls with outcome "follow_up_required".
    2. Extract customer/issue details from call notes and transcripts.
    3. Ask LLM to generate job details (title, description).
    4. Auto-create new jobs for follow-ups.
    """

    # ============================================================
    # STEP 1: Fetch all calls with outcome "follow_up_required"
    # ============================================================

    list_all_calls_tool = tools_by_name["call_log_server_list_calls"]

    logger.info("Fetching all calls to filter follow-up required")

    cursor = None
    all_calls = []

    while True:
        calls_result = await list_all_calls_tool.ainvoke(
            {
                "data": {
                    "limit": 100,
                    "cursor": cursor,
                }
            }
        )

        text = calls_result[0]["text"]

        # Convert JSON string → Python dict
        text_json = json.loads(text)

        # Fetch pagination information
        has_more = text_json["has_more"]
        next_cursor = text_json["next_cursor"]
        data = text_json["data"]

        logger.info(f"Fetched {len(data)} calls")

        all_calls.extend(data)

        if not has_more:
            break

        cursor = next_cursor

    logger.info(f"Total calls fetched: {len(all_calls)}")

    # Filter calls with outcome "follow_up_required"
    follow_up_calls = [
        call for call in all_calls
        if call.get("outcome") == "follow_up_required"
    ]

    logger.info(f"Follow-up required calls found: {len(follow_up_calls)}")

    if not follow_up_calls:
        logger.info("No follow-up required calls found.")
        return {
            "created_jobs": [],
            "follow_up_calls": [],
        }

    # ============================================================
    # STEP 2: Extract customer/issue details from calls
    # ============================================================

    call_details = []

    for call in follow_up_calls:
        details = {
            "call_id": call.get("call_id"),
            "customer_name": call.get("customer_name"),
            "phone_number": call.get("phone_number"),
            "agent_name": call.get("agent_name"),
            "transcript": call.get("transcript", ""),
            "notes": call.get("notes", []),
        }
        call_details.append(details)

    logger.info(f"Extracted details from {len(call_details)} follow-up calls")

    # ============================================================
    # STEP 3: Use LLM to generate job details
    # ============================================================

    prompt = f"""
You are processing customer service calls that require follow-up actions.

Your task is to extract customer issue details and generate job information.

Below are the follow-up required calls:

{json.dumps(call_details, indent=2)}

For EACH call, extract:

1. Issue Summary: Brief summary of what needs to be addressed
2. Priority Level: Determine if it should be "low", "medium", "high", or "critical"
3. Job Type: What kind of job needs to be created (e.g., "Callback", "Technical Support", "Product Replacement")

RULES:

1. Do not create more than one job per call.
2. Use the customer name in your analysis.
3. If transcript mentions urgent/critical issues, mark as high or critical priority.
4. Extract the actual problem/issue from transcript and notes.
5. Do not guess - use only information from the provided calls.

Return the result using the required structured output with a list of jobs to create.
"""

    structured_llm = llm.with_structured_output(
        FollowUpJobCreationOutput
    )

    response = structured_llm.invoke(prompt)

    logger.info(f"Follow-up Job Creation Response: {response}")

    if not response.jobs_to_create or len(response.jobs_to_create) == 0:
        logger.info("LLM did not identify any jobs to create.")
        return {
            "created_jobs": [],
            "follow_up_calls": follow_up_calls,
        }

    # ============================================================
    # STEP 4: Create jobs for each follow-up call
    # ============================================================

    create_job_tool = tools_by_name["job_server_create_job"]
    add_note_tool = tools_by_name["call_log_server_add_call_note"]

    created_jobs = []

    for idx, job_info in enumerate(response.jobs_to_create):
        try:
            # Generate unique job ID
            job_id = f"JOB-{int(uuid.uuid4().int) % 10000:04d}"

            # Create job description with follow-up details
            description = (
                f"Follow-up job for customer: {job_info.customer_name}\n"
                f"Issue: {job_info.issue_summary}\n"
                f"Related Call ID: {job_info.call_id}\n"
                f"Contact: {job_info.phone_number}"
            )

            logger.info(f"Creating job: {job_id} for customer {job_info.customer_name}")

            create_result = await create_job_tool.ainvoke(
                {
                    "data": {
                        "id": job_id,
                        "title": f"Follow-up: {job_info.job_type} - {job_info.customer_name}",
                        "description": description,
                        "priority": job_info.priority,
                    }
                }
            )

            logger.info(f"Job {job_id} created successfully: {create_result}")

            # Add note to the original call linking it to the job
            note_text = f"Follow-up job created: {job_id}"

            await add_note_tool.ainvoke(
                {
                    "data": {
                        "call_id": job_info.call_id,
                        "text": note_text,
                    }
                }
            )

            logger.info(f"Note added to call {job_info.call_id} linking to job {job_id}")

            created_jobs.append(
                {
                    "job_id": job_id,
                    "call_id": job_info.call_id,
                    "customer_name": job_info.customer_name,
                    "priority": job_info.priority,
                    "result": create_result,
                }
            )

        except Exception as e:
            logger.error(f"Error creating job for call {job_info.call_id}: {str(e)}")
            continue

    # ============================================================
    # Workflow Complete
    # ============================================================

    logger.info(f"Follow-up jobs workflow completed. Created {len(created_jobs)} jobs.")

    return {
        "created_jobs": created_jobs,
        "follow_up_calls": follow_up_calls,
        "jobs_count": len(created_jobs),
    }