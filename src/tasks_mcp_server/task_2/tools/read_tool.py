from typing import Union
from src.tasks_mcp_server.task_2.data import data as D
from src.tasks_mcp_server.task_2.schemas import tool_output_schemas as TS
from src.tasks_mcp_server.task_2.schemas.tool_input_schemas import PaginationInput
from src.tasks_mcp_server.task_2.schemas.error_schemas import ErrorResponse


def register_read_tools(mcp):

    @mcp.tool(
        annotations={
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        }
    )
    async def list_jobs(
        data: PaginationInput,
    ) -> Union[TS.JobsOutput, ErrorResponse]:
        """List jobs using cursor-based pagination."""

        try:
            start = int(data.cursor) if data.cursor else 0

            total_count = len(D.jobs)

            items = D.jobs[start:start + data.limit]

            next_position = start + len(items)

            has_more = next_position < total_count

            next_cursor = str(next_position) if has_more else None

            return TS.JobsOutput(
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
                error="Failed to list jobs",
                code="INTERNAL_ERROR",
                suggestion="Please try again later.",
            )


    @mcp.tool(
        annotations={
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        }
    )
    async def list_technicians(
        data: PaginationInput,
    ) -> Union[TS.TechniciansOutput, ErrorResponse]:
        """List all technicians using cursor-based pagination."""

        try:
            start = int(data.cursor) if data.cursor else 0

            total_count = len(D.technicians)

            data = D.technicians[start:start + data.limit]

            next_position = start + len(data)

            has_more = next_position < total_count

            next_cursor = str(next_position) if has_more else None

            return TS.TechniciansOutput(
                data=data,
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
                error="Failed to list technicians",
                code="INTERNAL_ERROR",
                suggestion="Please try again later.",
            )


    @mcp.tool(
        annotations={
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        }
    )
    async def get_available_technicians(
        data: PaginationInput,
    ) -> Union[TS.TechniciansOutput, ErrorResponse]:
        """List available technicians using cursor-based pagination."""

        try:
            available = [
                technician
                for technician in D.technicians
                if technician["available"]
            ]

            start = int(data.cursor) if data.cursor else 0

            total_count = len(available)

            items = available[start:start + data.limit]

            next_position = start + len(items)

            has_more = next_position < total_count

            next_cursor = str(next_position) if has_more else None

            return TS.TechniciansOutput(
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
                error="Failed to list available technicians",
                code="INTERNAL_ERROR",
                suggestion="Please try again later.",
            )


    @mcp.tool(
        annotations={
            "readOnlyHint": True,
            "destructiveHint": False,
            "idempotentHint": True,
            "openWorldHint": False,
        }
    )
    async def open_jobs(
        data: PaginationInput,
    ) -> Union[TS.JobsOutput, ErrorResponse]:
        """List open jobs using cursor-based pagination."""

        try:
            open_jobs = [
                job
                for job in D.jobs
                if job["status"] == "open"
            ]

            start = int(data.cursor) if data.cursor else 0

            total_count = len(open_jobs)

            items = open_jobs[start:start + data.limit]

            next_position = start + len(items)

            has_more = next_position < total_count

            next_cursor = str(next_position) if has_more else None

            return TS.JobsOutput(
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
                error="Failed to list open jobs",
                code="INTERNAL_ERROR",
                suggestion="Please try again later.",
            )