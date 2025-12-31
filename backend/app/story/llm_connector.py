import os
import requests
from dotenv import load_dotenv

LLM_URL = "https://llmfoundry.straive.com/groq/openai/v1/chat/completions"

PROJECT_ID = "puviintel"   
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(ROOT_DIR, ".env")
load_dotenv(ENV_PATH)
TOKEN = os.getenv("LLMFOUNDRY_TOKEN")


def call_llm(prompt: str):
    """
    Calls LLM Foundry (llama-3.3-70b-versatile) and returns the output text.
    """

    if not TOKEN:
        return "LLM Token not set. Please configure LLMFOUNDRY_TOKEN env variable."

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(LLM_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    
    except requests.exceptions.HTTPError as e:
        # Return full response text for debugging 500 errors
        try:
            error_detail = e.response.text
        except:
            error_detail = str(e)
        return f"LLM Request Failed: {e} - {error_detail}"
    
    except Exception as e:
        return f"LLM Request Failed: {e}"
