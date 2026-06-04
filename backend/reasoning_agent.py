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
You are a SENIOR SOC ANALYST.

Analyze ALL available evidence.

EMAIL:
{email}

IOC DATA:
{iocs}

THREAT SIGNALS:
{threat}

MEMORY PATTERNS:
{memory}

VIRUSTOTAL RESULTS:
{virustotal}

IMPORTANT:

- Do NOT automatically classify Google Forms as phishing.
- Do NOT automatically classify Gmail senders as phishing.
- External Gmail + Google Form alone is usually suspicious.
- Use VirusTotal reputation when making decisions.
- If VirusTotal malicious > 0, increase score.
- If VirusTotal suspicious > 0, increase score.
- If VirusTotal malicious == 0 and suspicious == 0,
  treat that as evidence that the URL is not currently
  known to be malicious.

RISK SCORE GUIDE:

0-30 = legit
31-60 = suspicious
61-100 = phishing

TASKS:

1. Determine verdict
2. Assign score
3. Extract signals
4. Generate SOC report bullets
5. Use all available evidence

Return STRICT JSON ONLY:

{{
  "verdict": "phishing|suspicious|legit",
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
                "content": "You are a senior SOC analyst."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content.strip()

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
            "soc_report": [
                "Reasoning output parsing failed."
            ],
            "confidence": 50
        }

    return {
        **state,
        "reasoning": result,
        "verdict": result.get("verdict", "suspicious"),
        "risk_score": result.get("score", 50)
    }