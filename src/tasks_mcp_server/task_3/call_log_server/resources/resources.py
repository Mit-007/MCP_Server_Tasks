from typing import Union
import json
from src.tasks_mcp_server.task_3.call_log_server.data import calls_data as D
from src.tasks_mcp_server.task_3.call_log_server.schemas.error_schemas import ErrorResponse


def register_resources(mcp):

    # ============================================================
    # 1. Recent Calls
    # ============================================================

    @mcp.resource("calls://recent/{n}",mime_type="application/json",)
    async def recent_calls(
        n: int,
    ) -> str:
        """Return the N most recent calls."""

        try:
            if n <= 0:
                error = ErrorResponse(
                    error="Invalid number of calls requested",
                    code="INVALID_LIMIT",
                    suggestion=(
                        "Provide a positive number of calls to retrieve."
                    ),
                )
                return json.dumps(error.model_dump())

            sorted_calls = sorted(
                D.calls,
                key=lambda call: call["started_at"],
                reverse=True,
            )

            recent = sorted_calls[:n]

            return json.dumps(recent)

        except KeyError:
            error = ErrorResponse(
                error=(
                    "Unable to retrieve recent calls: "
                    "required call field is missing"
                ),
                code="CALL_DATA_FIELD_MISSING",
                suggestion=(
                    "Verify that all call data contains "
                    "the required started_at field."
                ),
            )
            return json.dumps(error.model_dump())

        except TypeError:
            error = ErrorResponse(
                error=(
                    "Unable to retrieve recent calls: "
                    "invalid call data"
                ),
                code="INVALID_CALL_DATA",
                suggestion=(
                    "Verify that call data has the expected "
                    "dictionary structure."
                ),
            )
            return json.dumps(error.model_dump())

        except AttributeError:
            error = ErrorResponse(
                error=(
                    "Unable to retrieve recent calls: "
                    "call data is unavailable"
                ),
                code="CALL_DATA_UNAVAILABLE",
                suggestion=(
                    "Verify that the call data source is "
                    "available and try again."
                ),
            )
            return json.dumps(error.model_dump())

        except Exception:
            error = ErrorResponse(
                error=(
                    "Unable to retrieve recent calls: "
                    "an unexpected error occurred"
                ),
                code="INTERNAL_ERROR",
                suggestion=(
                    "Verify the call data and try again."
                ),
            )
            return json.dumps(error.model_dump())


    # ============================================================
    # 2. Failed Calls
    # ============================================================

    @mcp.resource(
        "calls://failed",
        mime_type="application/json",
    )
    async def failed_calls() -> str:
        """Return all calls with failed status."""

        try:
            failed = [
                call
                for call in D.calls
                if call["status"] == "failed"
            ]
            return json.dumps(failed)

        except KeyError:
            error = ErrorResponse(
                error=(
                    "Unable to retrieve failed calls: "
                    "required call status field is missing"
                ),
                code="CALL_STATUS_FIELD_MISSING",
                suggestion=(
                    "Verify that all call data contains "
                    "the required status field."
                ),
            )
            return json.dumps(error.model_dump())

        except TypeError:
            error = ErrorResponse(
                error=(
                    "Unable to retrieve failed calls: "
                    "invalid call data"
                ),
                code="INVALID_CALL_DATA",
                suggestion=(
                    "Verify that the call data has the expected "
                    "dictionary structure."
                ),
            )
            return json.dumps(error.model_dump())

        except AttributeError:
            error = ErrorResponse(
                error=(
                    "Unable to retrieve failed calls: "
                    "call data is unavailable"
                ),
                code="CALL_DATA_UNAVAILABLE",
                suggestion=(
                    "Verify that the call data source is "
                    "available and try again."
                ),
            )
            return json.dumps(error.model_dump())

        except Exception:
            error = ErrorResponse(
                error=(
                    "Unable to retrieve failed calls: "
                    "an unexpected error occurred"
                ),
                code="INTERNAL_ERROR",
                suggestion=(
                    "Verify the call data and try again."
                ),
            )
            return json.dumps(error.model_dump())