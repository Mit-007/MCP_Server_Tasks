from src.tasks_mcp_server.task_3.agent.services.llm import llm
from src.tasks_mcp_server.task_3.agent.core.logger import logger
from src.tasks_mcp_server.task_3.agent.schemas.workflow_schemas import (
    PendingCallsJobGenerationOutput,
)
import json
import uuid
from langchain.tools import tool

@tool
async def pending_calls_jobs_mapping_workflow(
    tools_by_name: dict = None,
):
    """
    Workflow: Pending Calls to Assigned Jobs Mapping with LLM

    1. Fetch all calls with status "pending".
    2. Use LLM to generate job details from pending calls.
    3. Create new jobs using LLM-generated data.
    4. Add call ID reference in job notes.
    5. Link the newly created jobs back to the original calls.
    """

    # ============================================================
    # STEP 1: Fetch all pending calls
    # ============================================================

    list_pending_calls_tool = tools_by_name["call_log_server_list_calls_by_status"]

    logger.info("Fetching all pending calls")

    cursor = None
    pending_calls_list = []

    while True:
        pending_calls_result = await list_pending_calls_tool.ainvoke(
            {
                "data": {
                    "status": "pending",
                    "limit": 100,
                    "cursor": cursor,
                }
            }
        )

        text = pending_calls_result[0]["text"]

        text_json = json.loads(text)

        has_more = text_json["has_more"]
        next_cursor = text_json["next_cursor"]
        data = text_json["data"]

        logger.info(f"Fetched {len(data)} pending calls")

        pending_calls_list.extend(data)

        if not has_more:
            break

        cursor = next_cursor

    logger.info(f"Total pending calls fetched: {len(pending_calls_list)}")

    if not pending_calls_list:
        logger.info("No pending calls found.")
        return {
            "created_jobs": [],
            "pending_calls": [],
            "workflow_summary": "No pending calls found.",
        }

    # ============================================================
    # STEP 2: Use LLM to generate job data for pending calls
    # ============================================================

    logger.info("Generating job data using LLM")

    prompt = f"""
You are processing pending customer service calls and generating job details.

Below are the pending calls that need to be converted into service jobs:

{json.dumps(pending_calls_list, indent=2)}

For EACH pending call, generate:

1. Job Title: A concise, professional title for the job
2. Job Description: Detailed description of what needs to be done (200-500 chars)
3. Priority: Determine if it should be "low", "medium", "high", or "critical"
4. Summary: Brief summary of why this job was created from this call

RULES:

1. Do NOT create more than one job per call.
2. Use the customer name and issue from the call.
3. Analyze the transcript to understand urgency and set priority accordingly.
4. If keywords like "urgent", "critical", "emergency", "asap" are present, set high or critical priority.
5. Job description should include actionable steps.
6. Do not hallucinate - use only information provided in the calls.
7. Return a professional, structured output.

For each job you generate, include:
- The call_id it corresponds to
- Customer name
- Generated job title
- Generated job description
- Priority level
- Reasoning for priority

Also generate an overall workflow summary explaining what jobs were identified and why.

Return the result using the required structured output format.
"""

    structured_llm = llm.with_structured_output(
        PendingCallsJobGenerationOutput
    )

    llm_response = structured_llm.invoke(prompt)

    logger.info(f"LLM Job Generation Response: {llm_response}")

    if not llm_response.jobs or len(llm_response.jobs) == 0:
        logger.info("LLM did not generate any jobs from pending calls.")
        return {
            "created_jobs": [],
            "pending_calls": pending_calls_list,
            "workflow_summary": llm_response.workflow_summary or "No jobs generated.",
        }

    # ============================================================
    # STEP 3: Create jobs using LLM-generated data
    # ============================================================

    create_job_tool = tools_by_name["job_server_create_job"]
    add_note_tool = tools_by_name["call_log_server_add_call_note"]

    created_jobs = []

    for job_info in llm_response.jobs:
        try:
            call_id = job_info.call_id
            customer_name = job_info.customer_name
            job_title = job_info.job_title
            job_description = job_info.job_description
            priority = job_info.priority
            reasoning = job_info.priority_reasoning

            # Generate unique job ID
            job_id = f"JOB-{int(uuid.uuid4().int) % 10000:04d}"

            # Enhance description with call metadata
            enhanced_description = (
                f"{job_description}\n\n"
                f"---\n"
                f"Source Call: {call_id}\n"
                f"Customer: {customer_name}\n"
                f"Priority Reasoning: {reasoning}"
            )

            logger.info(
                f"Creating job {job_id} for pending call {call_id} "
                f"from customer {customer_name} (Priority: {priority})"
            )

            # Create the job
            create_result = await create_job_tool.ainvoke(
                {
                    "data": {
                        "id": job_id,
                        "title": job_title,
                        "description": enhanced_description,
                        "priority": priority,
                    }
                }
            )

            logger.info(f"Job {job_id} created successfully")

            # ========================================================
            # STEP 4: Add call ID reference as note to the call
            # ========================================================

            note_text = (
                f"Job created: {job_id}\n"
                f"Title: {job_title}\n"
                f"Priority: {priority}"
            )

            # Add note to the pending call linking to the job
            await add_note_tool.ainvoke(
                {
                    "data": {
                        "call_id": call_id,
                        "text": note_text,
                    }
                }
            )

            logger.info(
                f"Note added to call {call_id} linking to job {job_id}"
            )

            created_jobs.append(
                {
                    "job_id": job_id,
                    "call_id": call_id,
                    "customer_name": customer_name,
                    "job_title": job_title,
                    "priority": priority,
                    "priority_reasoning": reasoning,
                    "result": create_result,
                }
            )

        except Exception as e:
            logger.error(
                f"Error creating job for pending call {job_info.call_id}: {str(e)}"
            )
            continue

    # ============================================================
    # Workflow Complete
    # ============================================================

    logger.info(
        f"Pending calls mapping workflow completed. "
        f"Created {len(created_jobs)} jobs from {len(pending_calls_list)} pending calls."
    )

    return {
        "created_jobs": created_jobs,
        "pending_calls": pending_calls_list,
        "jobs_created_count": len(created_jobs),
        "pending_calls_count": len(pending_calls_list),
        "workflow_summary": llm_response.workflow_summary,
    }