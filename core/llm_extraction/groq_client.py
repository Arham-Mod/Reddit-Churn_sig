import os
import logging
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path

# Force-load .env from project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_PATH)

def get_groq_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")

    logging.info(f"GROQ_API_KEY loaded: {bool(api_key)}")

    if not api_key:
        raise ValueError(
            f"GROQ_API_KEY not found. Checked path: {ENV_PATH}"
        )

    return Groq(api_key=api_key)
