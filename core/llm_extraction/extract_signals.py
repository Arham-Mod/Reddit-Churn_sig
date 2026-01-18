import json
import logging
from typing import List, Dict
from utils.logging import logger
import re

# -------------------------------------------------------
# Main public function
# -------------------------------------------------------

def analyze_text_for_churn(
    text: str,
    post_id: str,
    llm_client,
    return_raw: bool = False
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

    logging.info("========== RAW LLM OUTPUT ==========")
    logging.info(raw_output)
    logging.info("====================================")

    parsed = parse_llm_output(raw_output)
    validated = validate_llm_issues(parsed, post_id)

    if return_raw:
        return validated, raw_output

    return validated


# -------------------------------------------------------
# Prompt builder
# -------------------------------------------------------

def build_discussion_prompt(discussion: Dict) -> str:
    comments_text = "\n".join(
        f"- {c['body']}" for c in discussion["comments"][:50]
    )

    return f"""
You are an analyst identifying customer churn causes from a Reddit discussion.

TASK:
Analyze the discussion below and identify concrete issues that could cause users to stop using the product.

RULES:
- Only report issues explicitly mentioned by users.
- Do NOT infer or guess.
- If there is insufficient evidence, return an empty list.
- Each issue must include supporting quotes copied verbatim.

OUTPUT FORMAT (JSON ONLY):
{{
  "issues": [
    {{
      "issue_summary": "short description",
      "affected_feature": "specific feature or area",
      "problem_type": "bug | ux | pricing | performance | policy | other",
      "churn_severity": "low | medium | high",
      "confidence": "low | medium | high",
      "supporting_quotes": ["exact quote"]
    }}
  ]
}}

DISCUSSION:
Post Title: "{discussion['title']}"
Post Body: "{discussion['post_body']}"

Comments:
{comments_text}
"""

# -------------------------------------------------------
# LLM call wrapper
# -------------------------------------------------------

def call_llm(prompt: str, llm_client) -> str:
    """
    Sends the prompt to the LLM and returns raw text response.
    """

    try:
        response = llm_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile"
        )

        return response.choices[0].message.content

    except Exception as e:
        logging.error(f"LLM call failed: {e}")
        return ""


# -------------------------------------------------------
# Output parser
# -------------------------------------------------------



def parse_llm_output(raw_output: str) -> Dict:
    if not raw_output:
        return {"signals": []}

    cleaned = raw_output.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"signals": []}




# -------------------------------------------------------
# Validation & filtering
# -------------------------------------------------------

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

