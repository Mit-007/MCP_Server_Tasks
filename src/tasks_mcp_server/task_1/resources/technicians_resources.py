from src.tasks_mcp_server.task_1.data import data as D


def register_technicians_resources(mcp):

    @mcp.resource("technicians://available", mime_type="application/json")
    async def available_technicians():
        """Give list of all Available technicians."""
        try:
            return [
                technician
                for technician in D.technicians
                if technician["available"] is True
            ]

        except KeyError as exc:
            return (
                f"Unable to retrieve available technicians: required technician field is missing ({exc}).\n"
                f"Suggestion: verify that all technician data contains the required available field."
            )

        except TypeError as exc:
            return (
                f"Unable to retrieve available technicians: invalid technician data ({exc}).\n"
                f"Suggestion: verify that the technician data has the expected dictionary structure."
            )

        except AttributeError as exc:
            return (
                f"Unable to retrieve available technicians: technician data is unavailable ({exc}).\n"
                f"Suggestion: verify that the technician data source is available and try again."
            )

        except Exception as exc:
            return (
                f"Unable to retrieve available technicians: an unexpected error occurred ({exc}).\n"
                f"Suggestion: verify the technician data and try again."
            )