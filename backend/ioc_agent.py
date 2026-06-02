import re
import os
import json
from openai import OpenAI
from config import LLM_TEMPERATURE

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_iocs(state):

    text = state["email"]

    urls = re.findall(r"https?://\S+", text)
    emails = re.findall(r"[\w\.-]+@[\w\.-]+", text)

    prompt = f"""
You are a SOC IOC extraction engine.

Return ONLY valid JSON.

Email:
{text}

Extract:
- job_scam
- credential_request
- impersonation
- data_harvesting
- urgency_language
- summary
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=LLM_TEMPERATURE,
        messages=[
            {"role": "system", "content": "Extract phishing indicators."},
            {"role": "user", "content": prompt}
        ]
    )

    try:
        llm_data = json.loads(response.choices[0].message.content)
    except:
        llm_data = {
            "job_scam": False,
            "credential_request": False,
            "impersonation": False,
            "data_harvesting": False,
            "urgency_language": False,
            "summary": "parse_error"
        }

    return {
        **state,
        "iocs": {
            "urls": urls,
            "emails": emails,
            "features": llm_data
        }
    }