from app.prompts.base_prompt import JSON_RULES_FRAGMENT

def build_complaint_prompt(complaint: str) -> str:
    return f"""You are an AI assistant that extracts structured data from civic complaints.
Read the following complaint and extract the category, location, severity, and a brief summary.

{JSON_RULES_FRAGMENT}

Rules for extraction:
1. Category MUST be exactly one of: "Road & Infrastructure", "Water Supply", "Electricity", "Healthcare", "Education", "Transport", "Garbage Collection", "Sanitation", "Police", "Food Distribution", "Environment", "Government Office", "Other".
2. Severity MUST follow these rules:
   - "High": danger, accident, health risk, fire, electricity issue.
   - "Medium": public inconvenience, affects multiple citizens.
   - "Low": minor inconvenience, suggestion.
3. Summary MUST be exactly one clear, concise sentence.

Schema:
{{
  "category": "string (strictly from the allowed list)",
  "location": "string (extracted from text, or 'Unknown')",
  "severity": "string (High, Medium, or Low based on rules)",
  "summary": "string (exactly one sentence)"
}}

Complaint:
"{complaint}"
"""
