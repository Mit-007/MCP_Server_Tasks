from dotenv import load_dotenv
import os

load_dotenv()

TRANSPORT_TYPE = os.getenv("TRANSPORT_TYPE_JOB_SERVER")
if not TRANSPORT_TYPE:
    raise ValueError(
        "TRANSPORT_TYPE_JOB_SERVER environment variable is required. "
        "Suggestion: export TRANSPORT_TYPE_JOB_SERVER=STDIO or TRANSPORT_TYPE_JOB_SERVER=HTTP"
    )

TRANSPORT_PORT = None
if TRANSPORT_TYPE == "HTTP":
    TRANSPORT_PORT = int(os.getenv("TRANSPORT_PORT_JOB_SERVER"))
    if not TRANSPORT_PORT:
        raise ValueError(
            "TRANSPORT_PORT_JOB_SERVER environment variable is required when using HTTP transport. "
            "Suggestion: export TRANSPORT_PORT_JOB_SERVER=3000"
        )