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
You are a SENIOR SOC ANALYST in a Security Operations Center.

Your job is to classify emails using ALL available signals.

========================
EMAIL
========================
{email}

========================
IOC DATA
========================
{iocs}

========================
THREAT SIGNALS
========================
{threat}

========================
MEMORY MATCHES
========================
{memory}

========================
VIRUSTOTAL RESULTS
========================
{virustotal}

========================
IMPORTANT RULES (CRITICAL)
========================

1. VirusTotal is ONLY a weak signal:
   - Many phishing URLs are new and NOT detected yet.
   - Do NOT treat "clean VirusTotal" as safe.

2. Suspicious classification is VERY IMPORTANT:
   - If ANY uncertainty exists → prefer "suspicious"
   - Do NOT overuse "legit"

3. Mark as SUSPICIOUS if ANY of these exist:
   - External sender (Gmail or non-org domain)
   - Any form / survey / Google Form link
   - Any login, verification, HR, payroll, account-related context
   - Any data collection intent

4. Mark as PHISHING if:
   - Strong impersonation OR
   - Fake login pages OR
   - Clear credential harvesting OR
   - Known malicious patterns OR
   - Multiple high-risk signals combined

5. Mark as LEGIT ONLY IF:
   - No links
   - No external sender risk
   - No request for action
   - No sensitive context

6. Decision bias rule:
   - If unsure between legit vs suspicious → choose SUSPICIOUS
   - If unsure between suspicious vs phishing → choose SUSPICIOUS

========================
RISK SCORE GUIDE
========================
0–30 = legit
31–60 = suspicious
61–100 = phishing

========================
OUTPUT FORMAT (STRICT JSON ONLY)
========================
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
            "soc_report": ["Reasoning output parsing failed."],
            "confidence": 50
        }

    return {
        **state,
        "reasoning": result,
        "verdict": result.get("verdict", "suspicious"),
        "risk_score": result.get("score", 50)
    }