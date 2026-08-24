from src.tasks_mcp_server.task_3.agent.services.llm import llm
from src.tasks_mcp_server.task_3.agent.core.logger import logger
from src.tasks_mcp_server.task_3.agent.schemas.workflow_schemas import WorkflowLLmOutput
from src.tasks_mcp_server.task_3.agent.schemas.workflows_tools_schemas import LinkJobAndCallInput
from langchain.tools import tool

@tool
async def link_job_and_call_workflow(
    transcript: str,
    tools_by_name: dict = None,
):
    """
    Creates a customer call log, creates a related job,
    and links the job to the call using a call note.
    """
    
    try:
        structured_llm = llm.with_structured_output(
            WorkflowLLmOutput
        )
    except Exception as e:
        error_msg = f"Failed to initialize structured LLM: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"

    # ============================================================
    # STEP 1: CREATE CALL LOG
    # ============================================================

    try:
        log_call_tool = tools_by_name["call_log_server_log_call"]
        log_call_schema = log_call_tool.args_schema
    except KeyError as e:
        error_msg = f"Tool 'call_log_server_log_call' not found in tools_by_name: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"
    except Exception as e:
        error_msg = f"Failed to retrieve call log tool: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"

    call_prompt = f"""
You are responsible ONLY for creating a call log.

Read the customer call transcript and extract the information
required by the call logging tool.

CUSTOMER CALL TRANSCRIPT:
{transcript}

CALL LOG TOOL:
{log_call_tool.name}

CALL LOG TOOL DESCRIPTION:
{log_call_tool.description}

CALL LOG INPUT SCHEMA:
{log_call_schema}

Your job is to determine whether the transcript contains enough
information to create a valid call log.

If enough information is available:
- next = true
- args = valid arguments matching the call log tool schema

If required information is missing:
- next = false
- args = {{}}

Do not create job information.
Do not create call-note information.
Only prepare arguments for the call logging tool.
"""

    try:
        response = structured_llm.invoke(call_prompt)
    except Exception as e:
        error_msg = f"LLM failed to process call log prompt: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"

    print("CALL LOG LLM RESPONSE:")
    print(response)

    if not response.next:
        return "call log not created !!"

    try:
        logger.info(
            f"Creating call log with args: {response.args}"
        )

        call_result = await log_call_tool.ainvoke(
            response.args
        )

        logger.info(
            f"Call logged successfully: {call_result}"
        )
    except Exception as e:
        error_msg = f"Failed to create call log: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"


    # ============================================================
    # STEP 2: CREATE JOB
    # ============================================================

    try:
        create_job_tool = tools_by_name["job_server_create_job"]
        create_job_schema = create_job_tool.args_schema
    except KeyError as e:
        error_msg = f"Tool 'job_server_create_job' not found in tools_by_name: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"
    except Exception as e:
        error_msg = f"Failed to retrieve job creation tool: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"

    job_prompt = f"""
You are responsible ONLY for creating a service job.

Use the customer call transcript to determine what job should
be created.

CUSTOMER CALL TRANSCRIPT:
{transcript}

CREATED CALL:
{call_result}

JOB CREATION TOOL:
{create_job_tool.name}

JOB CREATION TOOL DESCRIPTION:
{create_job_tool.description}

JOB CREATION INPUT SCHEMA:
{create_job_schema}

Create a meaningful job based on the customer's problem.

For the job:
- Generate a unique job id.
- Create a concise and meaningful title.
- Create a useful description containing the actual customer issue.
- Select the appropriate priority based on the urgency described
  in the transcript.

If enough information is available:
- next = true
- args = valid arguments matching the job creation tool schema

If required information is missing:
- next = false
- args = {{}}

Do not create call-note information.
Do not modify the call log.
Only prepare arguments for the job creation tool.
"""

    try:
        response = structured_llm.invoke(job_prompt)
    except Exception as e:
        error_msg = f"LLM failed to process job creation prompt: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"

    print("JOB LLM RESPONSE:")
    print(response)

    if not response.next:
        return "job not created !!"

    try:
        logger.info(
            f"Creating job with args: {response.args}"
        )

        job_result = await create_job_tool.ainvoke(
            response.args
        )

        logger.info(
            f"Job created successfully: {job_result}"
        )
    except Exception as e:
        error_msg = f"Failed to create job: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"


    # ============================================================
    # STEP 3: LINK JOB TO CALL
    # ============================================================

    try:
        add_note_tool = tools_by_name[
            "call_log_server_add_call_note"
        ]
        add_note_schema = add_note_tool.args_schema
    except KeyError as e:
        error_msg = f"Tool 'call_log_server_add_call_note' not found in tools_by_name: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"
    except Exception as e:
        error_msg = f"Failed to retrieve add call note tool: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"

    link_prompt = f"""
You are responsible ONLY for linking an existing job
to an existing customer call.

The call and job have already been created successfully.

CUSTOMER CALL TRANSCRIPT:
{transcript}

CREATED CALL:
{call_result}

CREATED JOB:
{job_result}

CALL NOTE TOOL:
{add_note_tool.name}

CALL NOTE TOOL DESCRIPTION:
{add_note_tool.description}

CALL NOTE INPUT SCHEMA:
{add_note_schema}

Create a note for the call that clearly establishes the
relationship between the call and the job.

The note MUST contain the job_id of the created job.

Use the actual call_id of the created call.

The note should be concise, for example:

"Related job_id: <job_id>"

If enough information is available:
- next = true
- args = valid arguments matching the call-note tool schema

If required information is missing:
- next = false
- args = {{}}

Do not create another job.
Do not create another call.
Only prepare arguments for the call-note tool.
"""

    try:
        response = structured_llm.invoke(link_prompt)
    except Exception as e:
        error_msg = f"LLM failed to process link note prompt: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"

    print("LINK NOTE LLM RESPONSE:")
    print(response)

    if not response.next:
        return "call note not created !!"

    try:
        logger.info(
            f"Adding call note with args: {response.args}"
        )

        note_result = await add_note_tool.ainvoke(
            response.args
        )

        logger.info(
            f"Call note added successfully: {note_result}"
        )
    except Exception as e:
        error_msg = f"Failed to add call note: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"


    # ============================================================
    # WORKFLOW COMPLETE
    # ============================================================

    return {
        "call": call_result,
        "job": job_result,
        "note": note_result,
    }