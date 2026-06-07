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
You are an autonomous SOC reasoning engine inside a cybersecurity system.

You are NOT rule-based.
You are a decision-making SOC analyst.

Your job is to analyze all signals and produce a final classification.

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
INSTRUCTIONS
========================

- Analyze all signals together (do NOT use hardcoded rules)
- VirusTotal is only weak supporting evidence
- External sender or Google Forms may increase risk but are not decisive alone
- Think like a SOC analyst reviewing a real incident

Classify into EXACTLY ONE:

- legit
- suspicious
- phishing

IMPORTANT:
- verdict MUST be exactly one of: legit, suspicious, phishing
- NEVER return "error", "unknown", or null

========================
OUTPUT FORMAT (STRICT JSON ONLY)
========================

Return ONLY valid JSON:

{{
  "verdict": "legit | suspicious | phishing",
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
                "content": "You are a senior SOC analyst making final classification decisions."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content.strip()

    # Clean markdown fences if any
    content = (
        content.replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:
        result = json.loads(content)
    except Exception:
        # SAFE FALLBACK (prevents system crash)
        result = {
            "verdict": "suspicious",
            "score": 50,
            "signals": ["parse_error"],
            "soc_report": ["LLM output parsing failed; defaulting to suspicious."],
            "confidence": 50
        }

    # -----------------------------
    # HARD SAFETY GUARDS (IMPORTANT)
    # -----------------------------

    verdict = result.get("verdict", "suspicious")

    if verdict not in ["legit", "suspicious", "phishing"]:
        verdict = "suspicious"

    score = result.get("score", 50)

    if not isinstance(score, (int, float)):
        score = 50

    return {
        **state,
        "reasoning": result,
        "verdict": verdict,
        "risk_score": score
    }