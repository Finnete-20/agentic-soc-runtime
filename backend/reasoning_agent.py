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

Your job is to classify emails using reasoning over signals.

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
CRITICAL SOC CLASSIFICATION RULES
========================

PHISHING:
- login / password reset / account verification / Microsoft / Google / Zoom / DocuSign / bank / HR / payroll requests
- urgency + link
- impersonation
- credential or identity requests

SUSPICIOUS:
- external sender + link OR form OR request for action
- Google Forms or surveys
- mass email or unclear intent

LEGIT:
- internal communication only
- no links
- no actions required

IMPORTANT BIAS RULE:
- If link + action → NEVER legit
- If unsure between suspicious and phishing → choose phishing
- Do NOT overuse suspicious

VirusTotal is weak signal only.

========================
RISK SCORE GUIDE
========================
0–30 = legit
31–60 = suspicious
61–100 = phishing

========================
OUTPUT FORMAT (STRICT JSON ONLY)
========================

Return ONLY valid JSON. No markdown, no explanation.

Example:
{{
  "verdict": "phishing",
  "score": 85,
  "signals": ["external_sender", "login_link"],
  "soc_report": ["reason 1", "reason 2"],
  "confidence": 90
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=LLM_TEMPERATURE,
        messages=[
            {
                "role": "system",
                "content": "You are a senior SOC analyst specializing in phishing detection."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content.strip()

    # clean markdown if model adds it
    content = content.replace("```json", "").replace("```", "").strip()

    try:
        result = json.loads(content)

    except Exception as e:
        return {
            **state,
            "reasoning": {
                "verdict": "suspicious",
                "score": 55,
                "signals": ["parse_error"],
                "soc_report": [str(e)],
                "confidence": 60
            },
            "verdict": "suspicious",
            "risk_score": 55
        }

    verdict = result.get("verdict", "suspicious")
    score = result.get("score", 50)

    # =========================
    # SAFETY + CONSISTENCY FIX
    # =========================
    email_lower = email.lower()

    # force phishing for obvious attack patterns
    if any(k in email_lower for k in ["login", "verify", "reset", "password", "account"]):
        if verdict != "phishing":
            verdict = "phishing"
            score = max(score, 80)

    # normalize scoring consistency
    if verdict == "phishing" and score < 60:
        score = 85
    elif verdict == "suspicious" and score > 80:
        score = 65
    elif verdict == "legit" and score > 40:
        score = 25

    return {
        **state,
        "reasoning": result,
        "verdict": verdict,
        "risk_score": score
    }