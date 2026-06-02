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

Return ONLY valid JSON (no markdown, no explanation):

{{
  "job_scam": true,
  "credential_request": true,
  "impersonation": true,
  "data_harvesting": true,
  "urgency_language": true,
  "summary": "short security summary"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": "Extract phishing indicators. Return strict JSON only."},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content.strip()

    # ---------------------------
    # SAFE JSON CLEANING
    # ---------------------------
    content = content.replace("```json", "").replace("```", "").strip()

    try:
        llm_data = json.loads(content)
    except:
        llm_data = {
            "job_scam": "job" in text.lower(),
            "credential_request": any(k in text.lower() for k in ["password", "login", "verify"]),
            "impersonation": False,
            "data_harvesting": "email" in text.lower(),
            "urgency_language": "urgent" in text.lower(),
            "summary": "fallback_rule_based"
        }

    return {
        **state,
        "iocs": {
            "urls": urls,
            "emails": emails,
            "features": llm_data
        }
    }