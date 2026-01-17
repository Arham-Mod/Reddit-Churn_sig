import json
import logging
from typing import List, Dict
from utils.logging import logger
import re

# -------------------------------------------------------
# Main public function
# -------------------------------------------------------

def extract_churn_signals(
    text: str,
    taxonomy: List[Dict],
    llm_client
) -> List[Dict]:
    """
    Extract churn signals from a single text chunk using an LLM.

    Args:
        text (str): Cleaned reddit post or comment text
        taxonomy (list[dict]): Normalized churn taxonomy
        llm_client: Initialized LLM client (Groq or similar)

    Returns:
        List of validated churn signals:
        [
            {"id": "pricing_dissatisfaction", "confidence": 0.82}
        ]
    """

    if not text :
        logger.info("Empty text provided for signal extraction")
        return []
    
    

    prompt = build_extraction_prompt(text, taxonomy)

    raw_output = call_llm(prompt, llm_client)

    parsed_output = parse_llm_output(raw_output)

    final_signals = validate_and_filter_signals(parsed_output, taxonomy)

    
    return {
    "signals": final_signals,
    "features": parsed_output.get("features", []),
    "root_cause": parsed_output.get("root_cause")

}



# -------------------------------------------------------
# Prompt builder
# -------------------------------------------------------

def build_extraction_prompt(text: str, taxonomy: List[Dict]) -> str:
    """
    Builds a strict prompt for churn signal extraction.
    """

    allowed_signals = [
        f"- {item['id']}: {item['definition']}"
        for item in taxonomy
    ]

    signal_block = "\n".join(allowed_signals)

    prompt = f"""
You are a text classification system.

TASK:
Identify which churn signals are present in the given text.

ALLOWED SIGNALS:
{signal_block}

RULES:
- Only use signal IDs from the allowed list
- Do NOT invent new labels
- Return valid JSON only
- If no signals are present, return an empty list
- Confidence must be between 0 and 1

OUTPUT FORMAT:
{{
  "signals": [
    {{
      "id": "<signal_id>",
      "confidence": <float>
    }}
  ]
}}

TEXT TO ANALYZE:
\"\"\"{text}\"\"\"
"""

    return prompt.strip()


# -------------------------------------------------------
# LLM call wrapper
# -------------------------------------------------------

def call_llm(prompt: str, llm_client) -> str:
    """
    Sends the prompt to the LLM and returns raw text response.
    """

    try:
        response = llm_client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
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

def validate_and_filter_signals(
    extracted: Dict,
    taxonomy: List[Dict]
) -> List[Dict]:
    """
    Validate signal IDs, apply confidence thresholds,
    and enforce priority rules.
    """

    if "signals" not in extracted:
        return []

    taxonomy_map = {
        item["id"]: item for item in taxonomy
    }

    valid_signals = []

    for signal in extracted["signals"]:
        signal_id = signal.get("id")
        confidence = signal.get("confidence")

        if signal_id not in taxonomy_map:
            continue

        if not isinstance(confidence, (int, float)):
            continue

        threshold = taxonomy_map[signal_id]["confidence_threshold"]

        if confidence < threshold:
            continue

        valid_signals.append({
            "id": signal_id,
            "confidence": round(confidence, 2)
        })

    # Enforce priority rules
    valid_signals.sort(
        key=lambda x: taxonomy_map[x["id"]]["priority"]
    )

    # Remove churn_threat if explicit_exit_intent exists
    signal_ids = {s["id"] for s in valid_signals}
    if "explicit_exit_intent" in signal_ids:
        valid_signals = [
            s for s in valid_signals if s["id"] != "churn_threat"
        ]

    return valid_signals
