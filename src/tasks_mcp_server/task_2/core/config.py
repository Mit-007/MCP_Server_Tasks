from dotenv import load_dotenv
import os

load_dotenv()

TRANSPORT_TYPE = os.getenv("TRANSPORT_TYPE_JOB_SERVER")
TRANSPORT_PORT = None
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

if TRANSPORT_TYPE == "HTTP" :
    TRANSPORT_PORT = int(os.getenv("TRANSPORT_PORT_JOB_SERVER"))

