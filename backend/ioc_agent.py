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
You are a SOC IOC extraction assistant.

Email:
{text}

Extract structured intelligence:

Return JSON:
{{
  "suspicious_summary": "...",
  "risk_keywords": [],
  "phishing_indicators": []
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": "Extract cybersecurity indicators."},
            {"role": "user", "content": prompt}
        ]
    )

    llm_output = response.choices[0].message.content

    try:
        llm_data = json.loads(llm_output)
    except:
        llm_data = {
            "suspicious_summary": "parse_error",
            "risk_keywords": [],
            "phishing_indicators": []
        }

    return {
        **state,
        "iocs": {
            "urls": urls,
            "emails": emails,
            "llm": llm_data
        }
    }