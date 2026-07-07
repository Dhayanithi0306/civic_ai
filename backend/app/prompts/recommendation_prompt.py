import json

def build_recommendation_prompt(age: int, occupation: str, income: int, state: str, schemes: list) -> str:
    # Optimize tokens by sending only necessary fields
    optimized_schemes = []
    for s in schemes:
        optimized_schemes.append({
            "name": s.get("name"),
            "category": s.get("category"),
            "eligibility": s.get("eligibility"),
            "documents_required": s.get("documents_required", [])
        })
    schemes_json = json.dumps(optimized_schemes, indent=2)

    return f"""You are a smart scheme recommender.
Given the user's profile and the available schemes, recommend the TOP 3 matching schemes.
NEVER recommend schemes outside the provided list.

User Profile:
- Age: {age}
- Occupation: {occupation}
- Monthly Income: ₹{income}
- State: {state}

Available Schemes:
{schemes_json}

Respond ONLY with a valid JSON array matching exactly this schema:
[
  {{
    "name": "string (Exact name of the scheme)",
    "category": "string (The category of the scheme)",
    "eligibility_match_score": "string ('High', 'Medium', or 'Low')",
    "reason": "string (Explicitly explain WHY the user qualifies based on their profile)",
    "benefits": "string (Key benefits)",
    "documents_required": ["string", "string"],
    "application_guidance": "string (Brief steps or advice on how to apply)"
  }}
]

CRITICAL RULES:
- Do NOT include markdown formatting like ```json or ```.
- Do NOT include any explanations, prefixes, or extra text.
- ONLY output the raw JSON array.
"""
