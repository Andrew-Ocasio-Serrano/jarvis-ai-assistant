import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def validate_config():
    if not GROQ_API_KEY:
        raise EnvironmentError(
            "GROQ_API_KEY is not configured.\n"
            "Set it in your .env file — see .env.example."
        )