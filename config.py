
import os
from dotenv import load_dotenv

# Load .env file when running locally.
# Hugging Face supplies environment variables directly.
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DUFFEL_API_KEY = os.getenv("DUFFEL_API_KEY")
LITEAPI_API_KEY = os.getenv("LITEAPI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


def validate_api_keys():
    required_keys = {
        "GROQ_API_KEY": GROQ_API_KEY,
        "DUFFEL_API_KEY": DUFFEL_API_KEY,
        "LITEAPI_API_KEY": LITEAPI_API_KEY,
        "TAVILY_API_KEY": TAVILY_API_KEY,
        "OPENWEATHER_API_KEY": OPENWEATHER_API_KEY,
    }

    missing = [
        name
        for name, value in required_keys.items()
        if not value
    ]

    if missing:
        raise ValueError(
            "Missing API keys: " + ", ".join(missing)
        )
