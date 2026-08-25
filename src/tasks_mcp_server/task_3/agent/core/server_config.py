from dotenv import load_dotenv
import os
load_dotenv()

SERVERS = {
    "Task-2": {
        "transport": "streamable_http",
        "url": os.getenv("JOB_SERVER_URL"),
        "headers": {
            "AUTH_TOKEN": os.getenv("CALL_LOG_SERVER_AUTH_TOKEN"),
        },
    },

    "Task-3_call_log_server": {
        "transport": "streamable_http",
        "url": os.getenv("CALL_LOG_SERVER_URL"),
        "headers": {
            "AUTH_TOKEN": os.getenv("JOB_SERVER_AUTH_TOKEN"),
        },
    },
}
