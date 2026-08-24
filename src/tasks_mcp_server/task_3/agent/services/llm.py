from langchain_google_genai import ChatGoogleGenerativeAI
from src.tasks_mcp_server.task_3.agent.core.config import GOOGLE_API_KEY
from src.tasks_mcp_server.task_3.agent.core.logger import logger

try:
    if not GOOGLE_API_KEY:
        raise ValueError(
            "GOOGLE_API_KEY is missing. Please set it in your .env file."
        )

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        temperature=0
    )

except Exception as e:
    logger.error(f"Failed to initialize LLM: {e}")
    llm = None