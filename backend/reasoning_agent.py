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
You are an autonomous Security Operations Center (SOC) analyst powered by an LLM.

You are NOT a rule-based system.
You make reasoning-based security decisions like a real human analyst.

Your task is to classify the email into EXACTLY ONE label:

- legit
- suspicious
- phishing

========================
EMAIL
========================
{email}

========================
IOC SIGNALS
========================
{iocs}

========================
THREAT SIGNALS
========================
{threat}

========================
MEMORY SIGNALS
========================
{memory}

========================
VIRUSTOTAL DATA
========================
{virustotal}

========================
ANALYSIS INSTRUCTIONS
========================

Evaluate like a SOC analyst:
- Identify social engineering intent
- Detect impersonation or trust boundary violations
- Evaluate external links and data collection risks
- Do NOT rely on simple keyword rules
- Google Forms, surveys, login links may indicate risk
- Internal email does NOT automatically mean safe

You must reason contextually, not using fixed rules.

========================
OUTPUT FORMAT (STRICT JSON ONLY)
========================

{{
  "verdict": "legit | suspicious | phishing",
  "score": 0,
  "reasoning": "short SOC-style explanation",
  "signals": [],
  "confidence": 0
}}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=LLM_TEMPERATURE,
            messages=[
                {"role": "system", "content": "You are a senior SOC analyst."},
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content.strip()

       
        content = content.replace("```json", "").replace("```", "").strip()

        result = json.loads(content)

    except Exception:
        result = {
            "verdict": "suspicious",
            "score": 50,
            "reasoning": "LLM parsing failed or invalid response",
            "signals": ["parse_error"],
            "confidence": 50
        }

    # -------------------------
    
    # -------------------------
    verdict = str(result.get("verdict", "suspicious")).lower()

    if verdict not in ["legit", "suspicious", "phishing"]:
        verdict = "suspicious"

    result["verdict"] = verdict

    return {
        **state,
        "reasoning": result,
        "verdict": verdict,
        "risk_score": result.get("score", 50)
    }