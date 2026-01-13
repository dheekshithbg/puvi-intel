import os
import requests
from dotenv import load_dotenv

PROJECT_ID = "puviintel"   
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(ROOT_DIR, ".env")
load_dotenv(ENV_PATH)


def call_llm(prompt: str, token: str = None):
    """
    Calls LLM Foundry (llama-3.3-70b-versatile) and returns the output text.
    
    Args:
        prompt: The prompt to send to the LLM
        token: The LLM Foundry token (overrides env variable if provided)
    """
    # Use provided token or fallback to env variable
    llm_token = token or os.getenv("LLMFOUNDRY_TOKEN")

    if not llm_token:
        return "LLM Token not provided. Please provide a valid LLM Foundry Token."

    headers = {
        "Authorization": f"Bearer {llm_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }
    LLM_URL = os.getenv("LLM_URL")
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


