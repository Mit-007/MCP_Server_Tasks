from src.tasks_mcp_server.task_3.call_log_server.services.call_services import get_call 
from src.tasks_mcp_server.task_3.call_log_server.schemas.error_schemas import ErrorResponse
import json


def register_prompts(mcp):

    @mcp.prompt()
    async def quality_review(
        call_id: str,
    ) -> str:  
        """Generate a quality-review prompt for a customer call."""

        try:
            call = get_call(call_id)

            if call is None:
                error = ErrorResponse(
                    error=f"Call {call_id} was not found",
                    code="CALL_NOT_FOUND",
                    suggestion=(
                        "Provide a valid existing call ID. "
                        "Use list_calls to find available calls."
                    ),
                )
                return json.dumps(error.model_dump())

            notes = call.get("notes", [])

            notes_text = "\n".join(
                f"- {note['text']}"
                for note in notes
            ) if notes else "No notes available."

            return f"""
You are a customer support quality analyst.

Evaluate the following customer support call using ONLY the
information provided. Do not invent missing information.

CALL
---
Call ID: {call["call_id"]}
Customer: {call["customer_name"]}
Status: {call["status"]}
Outcome: {call["outcome"]}
Duration: {call["duration_seconds"]} seconds

CALL NOTES
---
{notes_text}

Evaluate the call using these three dimensions.

1. RESOLUTION
Give a score from 1 to 5.

1 = The customer's issue was not resolved.
5 = The customer's issue was completely resolved.

Explain the score using the call outcome and available notes.

2. CLARITY
Give a score from 1 to 5.

1 = The call information is unclear or poorly documented.
5 = The issue, handling, and result are very clear.

Explain the score using the available call information and notes.

3. DURATION
Give a score from 1 to 5.

1 = The duration appears highly inefficient for the issue.
5 = The duration appears appropriate and efficient.

If there is not enough information to judge the duration,
explicitly state that the duration cannot be confidently evaluated.

Return the result using exactly this structure:

Resolution:
Score: <1-5>
Reason: <explanation>

Clarity:
Score: <1-5>
Reason: <explanation>

Duration:
Score: <1-5>
Reason: <explanation>

Overall:
<short overall assessment>

Do not assume facts that are not present in the call data.
"""

        except ValueError:
            error = ErrorResponse(
                error="Invalid call ID",
                code="INVALID_CALL_ID",
                suggestion="Provide a valid call_id.",
            )
            return json.dumps(error.model_dump())

        except Exception as e:
            error = ErrorResponse(
                error="Failed to generate quality review prompt",
                code="INTERNAL_ERROR",
                suggestion="Please try again later.",
            )
            return json.dumps(error.model_dump())