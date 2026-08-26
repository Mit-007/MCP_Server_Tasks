from dotenv import load_dotenv
import os
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise EnvironmentError(
        "GOOGLE_API_KEY environment variable is not set. "
        "Please add it to your .env file."
    )