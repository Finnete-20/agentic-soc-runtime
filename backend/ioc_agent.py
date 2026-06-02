import re
import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_iocs(state):
    text = state["email"]

    urls = re.findall(r"https?://\S+", text)
    emails = re.findall(r"[\w\.-]+@[\w\.-]+", text)

    prompt = f"""
You are a SOC IOC extraction engine.

Analyze this email:

{text}

Return JSON ONLY:

{{
  "job_scam": true/false,
  "credential_request": true/false,
  "impersonation": true/false,
  "data_harvesting": true/false,
  "urgency_language": true/false,
  "summary": "short security summary"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
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