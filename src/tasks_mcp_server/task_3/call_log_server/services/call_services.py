from src.tasks_mcp_server.task_3.call_log_server.data import calls_data as D

def get_call(call_id: str):
    """
    Find and return a call by call_id.

    Returns:
        dict | None:
            Call record if found, otherwise None.
    """

    try:
        if not call_id:
            raise ValueError("call_id is required")

        call = next(
            (
                call
                for call in D.calls
                if call["call_id"] == call_id
            ),
            None,
        )

        return call

    except ValueError:
        raise

    except KeyError:
        raise ValueError(
            "Invalid call data: call_id field is missing"
        )

    except TypeError:
        raise ValueError(
            "Invalid call data structure"
        )

    except Exception:
        raise RuntimeError(
            "Failed to retrieve call"
        )