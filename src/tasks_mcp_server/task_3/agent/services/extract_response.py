import json
from typing import Any, Optional
 
 
def extract_response_text(response: Any, log_method: Optional[callable] = None) -> str:
    # ============================================================
    # Method 1: response.content[0]["text"]
    # ============================================================
    try:
        if hasattr(response, "content") and isinstance(response.content, list):
            if len(response.content) > 0:
                content_item = response.content[0]
                
                # Check if it's a dict with "text" key
                if isinstance(content_item, dict) and "text" in content_item:
                    if log_method:
                        log_method("Method 1: response.content[0]['text']")
                    return content_item["text"]
    
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
                    if log_method:
                        log_method("Method 2: response.content[0].text")
                    return content_item.text
    
    except (IndexError, TypeError, AttributeError):
        pass
    
    
    # ============================================================
    # Method 3: response.content (direct string)
    # ============================================================
    try:
        if hasattr(response, "content"):
            content = response.content
            
            # Check if it's directly a string
            if isinstance(content, str):
                if log_method:
                    log_method("Method 3: response.content (string)")
                return content
            
            # If it's a list with a single string item
            if isinstance(content, list) and len(content) > 0:
                if isinstance(content[0], str):
                    if log_method:
                        log_method("Method 3b: response.content[0] (string)")
                    return content[0]
    
    except (TypeError, AttributeError):
        pass
    
    
    # ============================================================
    # Method 4: response.text (alternative attribute)
    # ============================================================
    try:
        if hasattr(response, "text"):
            text = response.text
            if isinstance(text, str) and text.strip():
                if log_method:
                    log_method("Method 4: response.text")
                return text
    
    except (TypeError, AttributeError):
        pass
    
    
    # ============================================================
    # Method 5: Ultimate fallback (str conversion)
    # ============================================================
    try:
        result = str(response)
        if log_method:
            log_method("Method 5: str(response) - FALLBACK")
        return result
    
    except Exception as e:
        if log_method:
            log_method(f"All methods failed, returning error message")
        return f"[Error extracting response: {str(e)}]"