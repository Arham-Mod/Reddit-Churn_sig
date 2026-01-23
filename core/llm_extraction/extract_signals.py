import json
import logging
from typing import List, Dict
import re


def analyze_text_for_churn(
    text: str,
    post_id: str,
    llm_client,
) -> Dict:
    """
    Analyze a formatted discussion text chunk for churn-causing issues.
    """
    logging.info(
    f"[LLM ENTRY] post_id={post_id}, text_length={len(text)}"
)


    if not text or not text.strip():
        return {"post_id": post_id, "issues": []}

    prompt = build_discussion_prompt(text)

    raw_output = call_llm(prompt, llm_client)

    parsed = parse_llm_output(raw_output)
    
    validated = validate_llm_issues(parsed, post_id)

    return validated


def build_discussion_prompt(text: str) -> str:
    """
    Build LLM prompt for churn issue extraction from discussion text.
    """

    return f"""
You are a customer churn analyst. Extract product issues that indicate users may leave/cancel.

CRITICAL RULES:
1. Extract ONLY issues explicitly stated by users
2. Use exact quotes verbatim—no paraphrasing
3. Return valid JSON only—no markdown, no preamble
4. Empty list if no churn signals found

OUTPUT SCHEMA:
{{
  "issues": [
    {{
      "affected_feature": "string",
      "problem_type": "bug|UX|pricing|performance|support|policy|feature_removal|product_quality",
      "churn_severity": "low|medium|high",
      "supporting_quotes": ["exact quote 1", "exact quote 2"]
    }}
  ]
}}

SEVERITY GUIDE:
- HIGH: Explicitly threatens cancellation, blocks core workflow, breaks critical feature
- MEDIUM: Causes frustration, workarounds needed, degrades experience significantly  
- LOW: Minor annoyance, cosmetic issue, feature request

EXAMPLE INPUT:
"The new UI is confusing. I can't find my playlists anymore and might switch to Apple Music."

EXAMPLE OUTPUT:
{{
  "issues": [
    {{
      "affected_feature": "Navigation/UI",
      "problem_type": "UX",
      "churn_severity": "high",
      "supporting_quotes": ["I can't find my playlists anymore and might switch to Apple Music"]
    }}
  ]
}}

DISCUSSION TEXT:
\"\"\"
{text}
\"\"\"

JSON OUTPUT:""".strip()


def call_llm(prompt: str, llm_client) -> str:
    """
    Sends the prompt to the LLM and returns raw text response.
    """
    try:
        response = llm_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )

        content = response.choices[0].message.content

        if not isinstance(content, str):
            logging.error("LLM response content is not a string")
            return ""

        return content

    except Exception as e:
        logging.error(f"LLM call failed: {e}")
        return ""



def parse_llm_output(raw_output: str) -> Dict:
    if not raw_output:
        return {"issues": []}

    cleaned = raw_output.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"signals": []}




def validate_llm_issues(parsed: Dict, post_id: str) -> Dict:
    if "issues" not in parsed:
        return {"post_id": post_id, "issues": []}

    valid_issues = []

    for issue in parsed["issues"]:
        if not issue.get("supporting_quotes"):
            continue
        if issue.get("churn_severity") not in {"low", "medium", "high"}:
            continue

        valid_issues.append(issue)

    return {
        "post_id": post_id,
        "issues": valid_issues
    }

