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

    # SAFE prompt (no nested JSON formatting issues)
    prompt = f"""
You are a SENIOR SOC ANALYST in a Security Operations Center.

Your task is to classify emails into exactly ONE of:
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
VIRUSTOTAL
========================
{virustotal}

========================
CLASSIFICATION RULES
========================

1. If email is internal university/system message with NO external link → legit

2. If email has ANY external link OR external sender → at least suspicious

3. If phishing indicators exist (login page, credential request, fake Microsoft, HR/payroll, urgency) → phishing

4. Google Forms / surveys / data collection → suspicious

5. VirusTotal is weak signal (never trust alone)

6. NEVER output "benign" (invalid label)

7. If uncertain:
   suspicious > legit

========================
OUTPUT FORMAT (STRICT JSON ONLY)
========================
{{
  "verdict": "legit | suspicious | phishing",
  "score": 0,
  "signals": [],
  "soc_report": [],
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

        # clean markdown wrappers
        content = content.replace("```json", "").replace("```", "").strip()

        result = json.loads(content)

    except Exception:
        result = {
            "verdict": "suspicious",
            "score": 50,
            "signals": ["parse_error"],
            "soc_report": ["LLM parsing failed or invalid response"],
            "confidence": 50
        }

    # ✅ NORMALIZE LABELS (CRITICAL FIX)
    label_map = {
        "benign": "legit",
        "legit": "legit",
        "suspicious": "suspicious",
        "phishing": "phishing"
    }

    verdict = result.get("verdict", "suspicious")
    result["verdict"] = label_map.get(verdict, "suspicious")

    return {
        **state,
        "reasoning": result,
        "verdict": result["verdict"],
        "risk_score": result.get("score", 50)
    }