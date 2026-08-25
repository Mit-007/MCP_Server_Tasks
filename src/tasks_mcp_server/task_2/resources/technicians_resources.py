from typing import Union
import json

from src.tasks_mcp_server.task_2.data import data as D
from src.tasks_mcp_server.task_2.schemas.error_schemas import ErrorResponse


def register_technicians_resources(mcp):

    @mcp.resource(
        "technicians://available",
        mime_type="application/json",
    )
    async def available_technicians() -> str:
        """Give list of all Available technicians."""

        try:
            available_techs = [
                technician
                for technician in D.technicians
                if technician["available"] is True
            ]
            return json.dumps(available_techs)

        except KeyError:
            error = ErrorResponse(
                error=(
                    "Unable to retrieve available technicians: "
                    "required technician field is missing"
                ),
                code="TECHNICIAN_DATA_FIELD_MISSING",
                suggestion=(
                    "Verify that all technician data contains "
                    "the required available field."
                ),
            )
            return json.dumps(error.model_dump())

        except TypeError:
            error = ErrorResponse(
                error=(
                    "Unable to retrieve available technicians: "
                    "invalid technician data"
                ),
                code="INVALID_TECHNICIAN_DATA",
                suggestion=(
                    "Verify that the technician data has the expected "
                    "dictionary structure."
                ),
            )
            return json.dumps(error.model_dump())

        except AttributeError:
            error = ErrorResponse(
                error=(
                    "Unable to retrieve available technicians: "
                    "technician data is unavailable"
                ),
                code="TECHNICIAN_DATA_UNAVAILABLE",
                suggestion=(
                    "Verify that the technician data source is "
                    "available and try again."
                ),
            )
            return json.dumps(error.model_dump())

        except Exception:
            error = ErrorResponse(
                error=(
                    "Unable to retrieve available technicians: "
                    "an unexpected error occurred"
                ),
                code="INTERNAL_ERROR",
                suggestion=(
                    "Verify the technician data and try again."
                ),
            )
            return json.dumps(error.model_dump())