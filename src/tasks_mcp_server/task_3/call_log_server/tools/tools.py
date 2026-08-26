from datetime import datetime, timezone
from typing import Union
from src.tasks_mcp_server.task_3.call_log_server.data import calls_data as D
from src.tasks_mcp_server.task_3.call_log_server.schemas import tool_output_schemas as TS
from src.tasks_mcp_server.task_3.call_log_server.schemas.tool_input_schemas import (
    PaginationInput,
    LogCallInput,
    GetCallInput,
    CallsByStatusInput,
    UpdateCallOutcomeInput,
    DeleteCallInput,
    AddCallNoteInput,
    ListNotesInput,
    GetCallSummaryInput,
)
from src.tasks_mcp_server.task_3.call_log_server.schemas.error_schemas import ErrorResponse
from src.tasks_mcp_server.task_3.call_log_server.schemas.call_schemas import (
    CallStatus,
)
from src.tasks_mcp_server.task_3.call_log_server.core.logger import logger
from fastmcp import Context

def register_tools(mcp):

    # ============================================================
    # 1. log_call
    # ============================================================

    @mcp.tool(
        annotations={
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": False,
        }
    )
    async def log_call(
        data: LogCallInput,
    ) -> Union[TS.LogCallOutput, ErrorResponse]:
        """Create a new call log."""

        try:
            call_id = f"CALL-{len(D.calls) + 1:03d}"

            call = {
                "call_id": call_id,
                "customer_name": data.customer_name,
                "phone_number": data.phone_number,
                "agent_name": data.agent_name,
                "started_at": data.started_at,
                "duration_seconds": data.duration_seconds,
                "status": data.status.value,
                "outcome": (
                    data.outcome.value
                    if data.outcome
                    else None
                ),
                "transcript": data.transcript,
                "summary": None,
                "notes": [],
            }

            D.calls.append(call)

            return TS.LogCallOutput(
                data=call
            )

        except ValueError:
            return ErrorResponse(
                error="Invalid call data",
                code="INVALID_INPUT",
                suggestion="Provide valid call information.",
            )

        except Exception:
            return ErrorResponse(
                error="Failed to create call",
                code="INTERNAL_ERROR",
                suggestion="Please try again later.",
            )

    # ============================================================
    # 2. get_call
    # ============================================================

    @mcp.tool(
        annotations={
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        }
    )
    async def get_call(
        data: GetCallInput,
    ) -> Union[TS.GetCallOutput, ErrorResponse]:
        """Get a call by call_id."""

        try:
            call = next(
                (
                    call
                    for call in D.calls
                    if call["call_id"] == data.call_id
                ),
                None,
            )

            if call is None:
                return ErrorResponse(
                    error=f"Call {data.call_id} was not found",
                    code="CALL_NOT_FOUND",
                    suggestion="Provide a valid existing call_id.",
                )

            return TS.GetCallOutput(
                data=call
            )

        except ValueError:
            return ErrorResponse(
                error="Invalid call ID",
                code="INVALID_CALL_ID",
                suggestion="Provide a valid call_id.",
            )

        except Exception:
            return ErrorResponse(
                error="Failed to get call",
                code="INTERNAL_ERROR",
                suggestion="Please try again later.",
            )

    # ============================================================
    # 3. list_calls
    # ============================================================

    @mcp.tool(
        annotations={
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        }
    )
    async def list_calls(
        data: PaginationInput,
    ) -> Union[TS.CallsOutput, ErrorResponse]:
        """List calls using cursor-based pagination."""

        try:
            start = int(data.cursor) if data.cursor else 0

            total_count = len(D.calls)

            items = D.calls[
                start:start + data.limit
            ]

            next_position = start + len(items)

            has_more = next_position < total_count

            next_cursor = (
                str(next_position)
                if has_more
                else None
            )

            return TS.CallsOutput(
                data=items,
                next_cursor=next_cursor,
                has_more=has_more,
                total_count=total_count,
            )

        except ValueError:
            return ErrorResponse(
                error="Invalid cursor value",
                code="INVALID_CURSOR",
                suggestion="Provide a valid numeric cursor.",
            )

        except Exception:
            return ErrorResponse(
                error="Failed to list calls",
                code="INTERNAL_ERROR",
                suggestion="Please try again later.",
            )

    # ============================================================
    # 4. list_calls_by_status
    # ============================================================

    @mcp.tool(
        annotations={
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        }
    )
    async def list_calls_by_status(
        data: CallsByStatusInput,
    ) -> Union[TS.CallsOutput, ErrorResponse]:
        """List calls filtered by status using cursor pagination."""

        try:
            filtered_calls = [
                call
                for call in D.calls
                if call["status"] == data.status.value
            ]

            start = int(data.cursor) if data.cursor else 0

            total_count = len(filtered_calls)

            items = filtered_calls[
                start:start + data.limit
            ]

            next_position = start + len(items)

            has_more = next_position < total_count

            next_cursor = (
                str(next_position)
                if has_more
                else None
            )

            return TS.CallsOutput(
                data=items,
                next_cursor=next_cursor,
                has_more=has_more,
                total_count=total_count,
            )

        except ValueError:
            return ErrorResponse(
                error="Invalid cursor value",
                code="INVALID_CURSOR",
                suggestion="Provide a valid numeric cursor.",
            )

        except Exception:
            return ErrorResponse(
                error="Failed to list calls by status",
                code="INTERNAL_ERROR",
                suggestion="Please try again later.",
            )

    # ============================================================
    # 5. update_call_outcome
    # ============================================================

    @mcp.tool(
        annotations={
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        }
    )
    async def update_call_outcome(
        data: UpdateCallOutcomeInput,
    ) -> Union[TS.UpdateCallOutcomeOutput, ErrorResponse]:
        """Update the outcome of an existing call."""

        try:
            call = next(
                (
                    call
                    for call in D.calls
                    if call["call_id"] == data.call_id
                ),
                None,
            )

            if call is None:
                return ErrorResponse(
                    error=f"Call {data.call_id} was not found",
                    code="CALL_NOT_FOUND",
                    suggestion="Provide a valid existing call_id.",
                )

            call["outcome"] = data.outcome.value

            return TS.UpdateCallOutcomeOutput(
                data=call
            )

        except ValueError:
            return ErrorResponse(
                error="Invalid call outcome data",
                code="INVALID_INPUT",
                suggestion=(
                    "Provide a valid call_id and outcome."
                ),
            )

        except Exception:
            return ErrorResponse(
                error="Failed to update call outcome",
                code="INTERNAL_ERROR",
                suggestion="Please try again later.",
            )

    # ============================================================
    # 6. delete_call
    # ============================================================

    @mcp.tool(
        annotations={
            "readOnlyHint": False,
            "destructiveHint": True,
            "idempotentHint": False,
            "openWorldHint": False,
        }
    )
    async def delete_call(
        data: DeleteCallInput,
    ) -> Union[TS.DeleteCallOutput, ErrorResponse]:
        """Delete a call by call_id."""

        try:
            for index, call in enumerate(D.calls):

                if call["call_id"] == data.call_id:
                    D.calls.pop(index)

                    return TS.DeleteCallOutput(
                        data=True
                    )

            return ErrorResponse(
                error=f"Call {data.call_id} was not found",
                code="CALL_NOT_FOUND",
                suggestion="Provide a valid existing call_id.",
            )

        except ValueError:
            return ErrorResponse(
                error="Invalid call ID",
                code="INVALID_CALL_ID",
                suggestion="Provide a valid call_id.",
            )

        except Exception:
            return ErrorResponse(
                error="Failed to delete call",
                code="INTERNAL_ERROR",
                suggestion="Please try again later.",
            )

    # ============================================================
    # 7. add_call_note
    # ============================================================

    @mcp.tool(
        annotations={
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": False,
            "openWorldHint": False,
        }
    )
    async def add_call_note(
        data: AddCallNoteInput,
    ) -> Union[TS.AddCallNoteOutput, ErrorResponse]:
        """Add a note to an existing call."""

        try:
            call = next(
                (
                    call
                    for call in D.calls
                    if call["call_id"] == data.call_id
                ),
                None,
            )

            if call is None:
                return ErrorResponse(
                    error=f"Call {data.call_id} was not found",
                    code="CALL_NOT_FOUND",
                    suggestion="Provide a valid existing call_id.",
                )

            note_id = f"NOTE-{len(call['notes']) + 1:03d}"

            note = {
                "note_id": note_id,
                "text": data.text,
                "created_at": datetime.now(timezone.utc),
            }

            call["notes"].append(note)

            return TS.AddCallNoteOutput(
                data=note
            )

        except ValueError:
            return ErrorResponse(
                error="Invalid call note data",
                code="INVALID_INPUT",
                suggestion=(
                    "Provide a valid call_id and note."
                ),
            )

        except Exception:
            return ErrorResponse(
                error="Failed to add call note",
                code="INTERNAL_ERROR",
                suggestion="Please try again later.",
            )

    # ============================================================
    # 8. list_notes_for_call
    # ============================================================

    @mcp.tool(
        annotations={
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        }
    )
    async def list_notes_for_call(
        data: ListNotesInput,
    ) -> Union[TS.NotesOutput, ErrorResponse]:
        """List notes for a call using cursor pagination."""

        try:
            call = next(
                (
                    call
                    for call in D.calls
                    if call["call_id"] == data.call_id
                ),
                None,
            )

            if call is None:
                return ErrorResponse(
                    error=f"Call {data.call_id} was not found",
                    code="CALL_NOT_FOUND",
                    suggestion="Provide a valid existing call_id.",
                )

            notes = call["notes"]

            start = int(data.cursor) if data.cursor else 0

            total_count = len(notes)

            items = notes[
                start:start + data.limit
            ]

            next_position = start + len(items)

            has_more = next_position < total_count

            next_cursor = (
                str(next_position)
                if has_more
                else None
            )

            return TS.NotesOutput(
                data=items,
                next_cursor=next_cursor,
                has_more=has_more,
                total_count=total_count,
            )

        except ValueError:
            return ErrorResponse(
                error="Invalid cursor value",
                code="INVALID_CURSOR",
                suggestion="Provide a valid numeric cursor.",
            )

        except Exception:
            return ErrorResponse(
                error="Failed to list call notes",
                code="INTERNAL_ERROR",
                suggestion="Please try again later.",
            )

    # ============================================================
    # 9. get_call_summary
    # ============================================================

    @mcp.tool(
        annotations={
            "readOnlyHint": False,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        }
    )
    async def get_call_summary(
        data: GetCallSummaryInput,
        ctx: Context,
    ) -> Union[TS.CallSummaryOutput, ErrorResponse]:

        try:
            call = next(
                (
                    item
                    for item in D.calls
                    if item.get("call_id") == data.call_id
                ),
                None,
            )

            if call is None:
                return ErrorResponse(
                    error=f"Call {data.call_id} was not found",
                    code="CALL_NOT_FOUND",
                    suggestion="Provide a valid existing call_id.",
                )

            transcript = call.get("transcript")

            if not transcript or not str(transcript).strip():
                return ErrorResponse(
                    error="Call has no transcript",
                    code="TRANSCRIPT_NOT_FOUND",
                    suggestion=(
                        "Provide a call with a transcript "
                        "before generating a summary."
                    ),
                )

            prompt = f"""
    Summarize the following customer support call.

    Call ID: {call.get("call_id")}

    Customer:
    {call.get("customer_name", "Unknown")}

    Agent:
    {call.get("agent_name", "Unknown")}

    Duration:
    {call.get("duration_seconds", "Unknown")} seconds

    Status:
    {call.get("status", "Unknown")}

    Outcome:
    {call.get("outcome", "Unknown")}

    Transcript:
    {transcript}

    Generate a concise summary containing:

    1. Customer issue
    2. Actions taken by the agent
    3. Final outcome
    4. Important follow-up actions

    Do not invent information that is not present in the transcript.
    """
            try :
                result = await ctx.sample(
                    messages= prompt,
                    max_tokens=500,
                )  
            except:
                logger.warning("Sampling not supported by client")
                return ErrorResponse(
                    error="client does not support sampling",
                    code="CLIENT_NOT_SUPPORT",
                    suggestion="Avoid sampling for this client",
                )

            summary = result.result

            if not summary:
                return ErrorResponse(
                    error="The model returned an empty response",
                    code="EMPTY_SAMPLING_RESPONSE",
                    suggestion="Please try again.",
                )

            summary = summary.strip()

            call["summary"] = summary

            return TS.CallSummaryOutput(
                data=summary
            )

        except Exception as e:
            return ErrorResponse(
                error=f"Failed to generate call summary {e}",
                code="INTERNAL_ERROR",
                suggestion="Please try again later.",
            )

    # ============================================================
    # 10. get_stats
    # ============================================================

    @mcp.tool(
        annotations={
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        }
    )
    async def get_stats() -> Union[
        TS.StatsOutput,
        ErrorResponse,
    ]:
        """Return call counts by status and outcome."""

        try:
            status_counts = {
                status.value: 0
                for status in CallStatus
            }

            outcome_counts = {
                "resolved": 0,
                "unresolved": 0,
                "escalated": 0,
                "follow_up_required": 0,
                "no_answer": 0,
            }

            for call in D.calls:

                status = call.get("status")

                if status in status_counts:
                    status_counts[status] += 1

                outcome = call.get("outcome")

                if outcome in outcome_counts:
                    outcome_counts[outcome] += 1

            stats = TS.StatsData(
                total_calls=len(D.calls),
                by_status=TS.StatusStats(
                    pending=status_counts["pending"],
                    in_progress=status_counts["in_progress"],
                    completed=status_counts["completed"],
                    failed=status_counts["failed"],
                    cancelled=status_counts["cancelled"],
                ),
                by_outcome=TS.OutcomeStats(
                    resolved=outcome_counts["resolved"],
                    unresolved=outcome_counts["unresolved"],
                    escalated=outcome_counts["escalated"],
                    follow_up_required=outcome_counts[
                        "follow_up_required"
                    ],
                    no_answer=outcome_counts["no_answer"],
                ),
            )

            return TS.StatsOutput(
                data=stats
            )

        except Exception:
            return ErrorResponse(
                error="Failed to get call statistics",
                code="INTERNAL_ERROR",
                suggestion="Please try again later.",
            )