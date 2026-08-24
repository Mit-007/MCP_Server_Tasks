from src.tasks_mcp_server.task_3.agent.services.llm import llm
from src.tasks_mcp_server.task_3.agent.core.logger import logger
from src.tasks_mcp_server.task_3.agent.schemas.workflow_schemas import (
    CallStatsReportGenerationOutput,
)
import json
from datetime import datetime
from langchain.tools import tool

@tool
async def call_stats_job_impact_report_workflow(
    tools_by_name: dict = None,
):
    """
    Workflow: Call Statistics and Job Impact Report (LLM-Enhanced)

    1. Get call statistics (completed, failed, pending counts by status and outcome).
    2. Fetch all open jobs.
    3. Use LLM to generate comprehensive summary report with correlation analysis.
    """
    # ============================================================
    # STEP 1: Get call statistics
    # ============================================================

    get_stats_tool = tools_by_name["call_log_server_get_stats"]

    logger.info("Fetching call statistics")

    stats_result = await get_stats_tool.ainvoke({})

    stats_text = stats_result[0]["text"]
    
    # Convert JSON string → Python dict
    stats_json = json.loads(stats_text)

    logger.info(f"Call Statistics: {stats_json}")

    # ============================================================
    # STEP 2: Fetch all open jobs
    # ============================================================

    list_open_jobs_tool = tools_by_name["job_server_open_jobs"]

    logger.info("Fetching all open jobs")

    cursor = None
    open_jobs_list = []

    while True:
        open_jobs_result = await list_open_jobs_tool.ainvoke(
            {
                "data": {
                    "limit": 100,
                    "cursor": cursor,
                }
            }
        )

        text = open_jobs_result[0]["text"]

        # Convert JSON string → Python dict
        text_json = json.loads(text)

        # Fetch pagination information
        has_more = text_json["has_more"]
        next_cursor = text_json["next_cursor"]
        data = text_json["data"]

        logger.info(f"Fetched {len(data)} open jobs")

        open_jobs_list.extend(data)

        if not has_more:
            break

        cursor = next_cursor

    logger.info(f"Total open jobs fetched: {len(open_jobs_list)}")

    # ============================================================
    # STEP 3: Use LLM to generate comprehensive report
    # ============================================================

    logger.info("Generating report using LLM")

    prompt = f"""
You are a business analyst generating a comprehensive operational report.

Analyze the following call statistics and job data, then generate a detailed report.

CALL STATISTICS:
{json.dumps(stats_json, indent=2)}

OPEN JOBS DATA:
{json.dumps(open_jobs_list, indent=2)}

Generate a comprehensive report that includes:

1. CALL STATISTICS SUMMARY:
   - Total calls by status (pending, in_progress, completed, failed, cancelled)
   - Total calls by outcome (resolved, unresolved, escalated, follow_up_required, no_answer)
   - Key call metrics and trends

2. JOB STATISTICS SUMMARY:
   - Total open jobs count
   - Jobs by priority (low, medium, high, critical)
   - Assigned vs unassigned jobs count
   - Assignment rate percentage

3. CORRELATION ANALYSIS:
   - Relationship between pending calls and open jobs
   - Relationship between failed calls and high/critical priority jobs
   - Resource utilization insights
   - Capacity assessment (sufficient resources or overloaded)

4. CRITICAL OBSERVATIONS:
   - Identify bottlenecks
   - Highlight resource gaps
   - Note any critical risks
   - Flag urgent situations requiring immediate attention

5. RECOMMENDATIONS:
   - Specific actions to improve operations
   - Resource allocation suggestions
   - Priority handling recommendations
   - Follow-up action items

6. OVERALL SUMMARY:
   - Executive summary of operational health
   - Key findings
   - Impact assessment

Ensure the report is:
- Actionable and data-driven
- Professional and structured
- Based only on provided data (no hallucinations)
- Clearly identifies problems and solutions

Return the result using the required structured output format.
"""

    structured_llm = llm.with_structured_output(
        CallStatsReportGenerationOutput
    )

    llm_report = structured_llm.invoke(prompt)

    logger.info(f"LLM Report Generated: {llm_report}")

    # ============================================================
    # Workflow Complete
    # ============================================================

    return {
        "report": {
            "timestamp": datetime.utcnow().isoformat(),
            "call_statistics_summary": llm_report.call_statistics_summary,
            "job_statistics_summary": llm_report.job_statistics_summary,
            "correlation_analysis": llm_report.correlation_analysis,
            "critical_observations": llm_report.critical_observations,
            "recommendations": llm_report.recommendations,
            "overall_summary": llm_report.overall_summary,
        },
        "raw_stats": stats_json,
        "raw_jobs": open_jobs_list,
    }