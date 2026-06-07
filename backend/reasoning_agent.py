import os
import json
from openai import OpenAI
from config import LLM_TEMPERATURE

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def reasoning_agent(state):

    email = state.get("email", "")
    iocs = state.get("iocs", {})
    threat = state.get("threat", {})
    memory = state.get("memory", {})
    virustotal = state.get("virustotal", [])

    prompt = f"""
You are a SENIOR SOC ANALYST working in a Security Operations Center.

Your job is to classify emails into EXACTLY ONE of:
- legit
- suspicious
- phishing

You must be STRICT and CONSISTENT.

========================
CLASSIFICATION RULES
========================

🚨 PHISHING (score 61–100):
- Credential theft (password reset, login pages, account locked)
- Fake Microsoft, Google, bank, Zoom, HR impersonation
- ANY urgency + link asking to verify identity
- ANY login/verification link that is not official domain

⚠️ SUSPICIOUS (31–60):
- External Gmail sender + link present
- Google Forms or surveys requesting data
- Urgent tone but no direct credential theft
- Unknown link with no VirusTotal evidence

✅ LEGIT (0–30):
- Internal communication
- No external links
- No urgency
- No credential requests

========================
IMPORTANT OVERRIDES
========================

- VirusTotal is a STRONG SIGNAL:
  - malicious > 0 → increase likelihood of phishing
  - suspicious > 0 → increase likelihood of phishing/suspicious
  - harmless high AND undetected → NOT enough to mark phishing alone

- DO NOT automatically treat Google Forms as phishing
- DO NOT automatically treat Gmail sender as phishing
- BUT combination of Gmail + form + data harvesting = suspicious

========================
DATA
========================

EMAIL:
{email}

IOC:
{iocs}

THREAT:
{threat}

MEMORY:
{memory}

VIRUSTOTAL:
{virustotal}

========================
OUTPUT FORMAT (STRICT JSON ONLY)
========================

{{
  "verdict": "legit|suspicious|phishing",
  "score": 0,
  "signals": [],
  "soc_report": [],
  "confidence": 0
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=LLM_TEMPERATURE,
        messages=[
            {
                "role": "system",
                "content": "You are a strict SOC analyst. You MUST follow classification rules exactly."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content.strip()

    # clean markdown if model adds it
    content = (
        content.replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:
        result = json.loads(content)

    except Exception:
        result = {
            "verdict": "suspicious",
            "score": 50,
            "signals": ["parse_error"],
            "soc_report": ["Failed to parse LLM output"],
            "confidence": 50
        }

    return {
        **state,
        "reasoning": result,
        "verdict": result.get("verdict", "suspicious"),
        "risk_score": result.get("score", 50)
    }