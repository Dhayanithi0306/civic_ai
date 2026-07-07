import json
from app.prompts.base_prompt import GOVERNMENT_ASSISTANT_PERSONA

def build_chat_prompt(message: str, history: list, schemes: list) -> str:
    schemes_json = json.dumps(schemes, indent=2)
    
    formatted_history = ""
    if history:
        # only keep last 5 exchanges
        for h in history[-5:]:
            if hasattr(h, "role"):
                role = h.role
                content = h.content
            else:
                role = h.get("role", "user")
                content = h.get("content", "")
            formatted_history += f"{role.capitalize()}: {content}\n"
    
    return f"""{GOVERNMENT_ASSISTANT_PERSONA}

Available Government Schemes (Context):
{schemes_json}

Chat History:
{formatted_history}

User: {message}

Assistant (respond in plain text, do not output JSON):
"""
