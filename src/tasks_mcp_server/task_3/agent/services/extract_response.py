from typing import Any
from src.tasks_mcp_server.task_3.agent.core.logger import logger


def extract_response_text(response: Any) -> str:
    # ============================================================
    # Method 1: response.content[0]["text"]
    # ============================================================
    try:
        if hasattr(response, "content") and isinstance(response.content, list):
            if len(response.content) > 0:
                content_item = response.content[0]
                
                # Check if it's a dict with "text" key
                if isinstance(content_item, dict) and "text" in content_item:
                    text = content_item["text"]
                    if text is not None:
                        logger.debug("Response structure: response.content[0]['text']")
                        return str(text)
    
    except (IndexError, TypeError, AttributeError, KeyError):
        pass
    
    # ============================================================
    # Method 2: response.content[0].text
    # ============================================================
    try:
        if hasattr(response, "content") and isinstance(response.content, list):
            if len(response.content) > 0:
                content_item = response.content[0]
                
                # Check if it's an object with .text attribute
                if hasattr(content_item, "text"):
                    text = content_item.text
                    if text is not None:
                        logger.debug("Response structure: response.content[0].text")
                        return str(text)
    
    except (IndexError, TypeError, AttributeError):
        pass
    
    # ============================================================
    # Method 3: response.content (direct string or list)
    # ============================================================
    try:
        if hasattr(response, "content"):
            content = response.content
            
            # Check if it's directly a string
            if isinstance(content, str) and content is not None:
                logger.debug("Response structure: response.content (direct string)")
                return content
            
            # If it's a list with a single string item
            if isinstance(content, list) and len(content) > 0:
                if isinstance(content[0], str) and content[0] is not None:
                    logger.debug("Response structure: response.content[0] (string from list)")
                    return content[0]
    
    except (TypeError, AttributeError):
        pass
    
    # ============================================================
    # Method 4: response.text (alternative attribute)
    # ============================================================
    try:
        if hasattr(response, "text"):
            text = response.text
            if text is not None and isinstance(text, str):
                logger.debug("Response structure: response.text")
                return text
    
    except (TypeError, AttributeError):
        pass
    
    # ============================================================
    # Method 5: response.choices[0].message.content (OpenAI/Anthropic API)
    # ============================================================
    try:
        if hasattr(response, "choices") and isinstance(response.choices, list):
            if len(response.choices) > 0:
                choice = response.choices[0]
                
                # Check for .message.content pattern
                if hasattr(choice, "message") and hasattr(choice.message, "content"):
                    text = choice.message.content
                    if text is not None:
                        logger.debug("Response structure: response.choices[0].message.content")
                        return str(text)
    
    except (IndexError, TypeError, AttributeError):
        pass
    
    # ============================================================
    # Method 6: response.choices[0]["message"]["content"] (dict variant)
    # ============================================================
    try:
        if hasattr(response, "choices") and isinstance(response.choices, list):
            if len(response.choices) > 0:
                choice = response.choices[0]
                
                if isinstance(choice, dict) and "message" in choice:
                    message = choice["message"]
                    if isinstance(message, dict) and "content" in message:
                        text = message["content"]
                        if text is not None:
                            logger.debug("Response structure: response.choices[0]['message']['content']")
                            return str(text)
    
    except (IndexError, TypeError, AttributeError, KeyError):
        pass
    
    # ============================================================
    # Method 7: Ultimate fallback (str conversion)
    # ============================================================
    try:
        result = str(response)
        if result and result != "None":
            logger.warning("Response structure: Using fallback str(response) conversion")
            return result
    
    except Exception as e:
        logger.error(f"Failed to extract response text: {str(e)}")
        return f"[Error extracting response: {str(e)}]"