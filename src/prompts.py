from __future__ import annotations


SYSTEM_PROMPT = """You are a senior pre-sales document analyst.
You help Sales Engineers, Solutions Engineers, Solution Architects, and Bid Managers analyze procurement documents.
Return only valid JSON. Do not include Markdown fences."""


def build_user_prompt(
    *,
    text: str,
    document_type: str,
    detected_language: str,
    response_language: str,
) -> str:
    clipped_text = text[:120000]
    return f"""
Analyze the procurement document below.

Known metadata:
- Document type detected by local rules: {document_type}
- Source language detected by local rules: {detected_language}
- Required response language detected by local rules: {response_language}

Generate every field in the required response language: {response_language}.
Do not invent product names. Use generic architectural language for the solution outline.

Return a JSON object with this schema:
{{
  "executive_summary": {{
    "customer_overview": "",
    "opportunity_overview": "",
    "key_objectives": [""],
    "major_requirements": [""],
    "risks": [""],
    "recommendations": [""]
  }},
  "document_type": "RFP | RFI | Government Tender | Unknown",
  "detected_language": "English | Portuguese | Spanish",
  "response_language": "English | Portuguese | Spanish",
  "customer_context": {{
    "organization": "",
    "industry": "",
    "business_problem": "",
    "procurement_goal": ""
  }},
  "key_dates": [
    {{"name": "", "date": "", "notes": ""}}
  ],
  "requirements": [
    {{
      "requirement_id": "",
      "category": "Technical | Commercial | Security | Legal | Compliance | Other",
      "requirement_description": "",
      "mandatory_or_optional": "Mandatory | Optional | Unknown",
      "fit_assessment": "Good fit | Partial fit | Gap | Needs review",
      "notes": ""
    }}
  ],
  "risks": [
    {{
      "risk_id": "",
      "description": "",
      "impact": "",
      "probability": "High | Medium | Low | Unknown",
      "mitigation": "",
      "owner": "Sales | SE | Legal | Security | Product | Delivery | Customer | Unknown"
    }}
  ],
  "clarification_questions": [
    {{
      "question": "",
      "reason": "",
      "owner": "Sales | SE | Legal | Security | Product | Delivery | Customer"
    }}
  ],
  "go_no_go": {{
    "recommendation": "GO | CONDITIONAL GO | NO-GO",
    "executive_recommendation": "",
    "key_strengths": [""],
    "key_concerns": [""],
    "recommended_next_actions": [""]
  }},
  "solution_outline": {{
    "overview": "",
    "approach": [""],
    "architecture_components": [""],
    "delivery_considerations": [""],
    "assumptions": [""]
  }},
  "recommended_next_steps": [""]
}}

Document text:
{clipped_text}
"""
