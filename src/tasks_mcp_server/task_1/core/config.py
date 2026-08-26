from dotenv import load_dotenv
import os

load_dotenv()

TRANSPORT_TYPE = os.getenv("TRANSPORT_TYPE_JOB_SERVER").upper()
if not TRANSPORT_TYPE:
    raise ValueError("TRANSPORT_TYPE must be set to 'STDIO' or 'HTTP'")

TRANSPORT_PORT = None
if TRANSPORT_TYPE == "HTTP":
    port_str = os.getenv("TRANSPORT_PORT_JOB_SERVER")
    try:
        TRANSPORT_PORT = int(port_str)
    except ValueError:
        raise ValueError(f"TRANSPORT_PORT must be a valid integer, got: {port_str}")