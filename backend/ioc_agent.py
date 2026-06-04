import re
import os
import json
from openai import OpenAI
from config import LLM_TEMPERATURE


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY missing")
    return OpenAI(api_key=api_key)


def safe_json_parse(content):
    """
    Robust JSON parser for LLM output
    """
    try:
        return json.loads(content)
    except:
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass

    return {}


def extract_iocs(state):

    client = get_openai_client()

    text = state["email"]

    urls = re.findall(r"https?://\S+", text)
    emails = re.findall(r"[\w\.-]+@[\w\.-]+", text)

    prompt = f"""
You are a SOC IOC extraction engine.

Return ONLY valid JSON.

Email:
{text}

Extract:
- job_scam (true/false)
- credential_request (true/false)
- impersonation (true/false)
- data_harvesting (true/false)
- urgency_language (true/false)
- summary (string)
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=LLM_TEMPERATURE,
            messages=[
                {"role": "system", "content": "Return only JSON."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content

        llm_data = safe_json_parse(content)

    except Exception as e:
        print("IOC ERROR:", e)

        llm_data = {
            "job_scam": False,
            "credential_request": False,
            "impersonation": False,
            "data_harvesting": False,
            "urgency_language": False,
            "summary": "error"
        }

    return {
        **state,
        "iocs": {
            "urls": urls,
            "emails": emails,
            "features": llm_data
        }
    }