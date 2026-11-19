import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def get_client():
    return OpenAI(
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url=os.getenv(
                "LLM_BASE_URL",
                "https://openrouter.ai/api/v1"
            )
        )