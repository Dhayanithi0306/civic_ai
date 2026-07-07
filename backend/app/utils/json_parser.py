import json
import logging
import re

logger = logging.getLogger(__name__)

def safe_json_parse(text: str):
    """
    Safely extract and parse JSON from a string that might contain markdown or extra text.
    """
    logger.debug(f"Attempting to parse JSON from raw text: {text}")
    
    # 1. Try to find JSON within markdown fences
    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
    if json_match:
        extracted = json_match.group(1).strip()
    else:
        # 2. Try to find the first { or [ and extract until the end
        start_idx = text.find('{')
        start_list_idx = text.find('[')
        
        if start_idx == -1 and start_list_idx == -1:
            logger.error("No JSON-like structure found in text.")
            raise ValueError("No JSON structure found.")
            
        # Determine if it's an object or list
        if start_idx != -1 and (start_list_idx == -1 or start_idx < start_list_idx):
            extracted = text[start_idx:]
            # basic bracket matching to find the end
            end_idx = extracted.rfind('}')
            if end_idx != -1:
                extracted = extracted[:end_idx+1]
        else:
            extracted = text[start_list_idx:]
            end_idx = extracted.rfind(']')
            if end_idx != -1:
                extracted = extracted[:end_idx+1]

    extracted = extracted.strip()
    
    try:
        parsed = json.loads(extracted)
        logger.debug(f"Successfully parsed JSON: {parsed}")
        return parsed
    except json.JSONDecodeError as e:
        logger.error(f"JSON Parsing failed on cleaned text: {extracted}")
        raise ValueError(f"Failed to decode JSON: {str(e)}")
