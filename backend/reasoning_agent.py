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

You are NOT a rule-based classifier.
You are a decision-making SOC analyst.

Your job is to analyze all signals and make a final judgment.

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

You must:
- Analyze all signals holistically
- Detect phishing patterns, social engineering, and suspicious intent
- Avoid relying on any single signal (including VirusTotal)
- Reason like a human SOC analyst

Guidance:
- VirusTotal is only supporting evidence, not ground truth
- External sender may increase risk but is not decisive alone
- Google Forms / surveys can be legitimate OR malicious depending on context
- Do NOT use fixed thresholds or hardcoded rules

Classify the email as one of:
- "legit"
- "suspicious"
- "phishing"

========================
OUTPUT FORMAT (STRICT JSON ONLY)
========================

Return ONLY valid JSON:

{
  "verdict": "legit | suspicious | phishing",
  "score": 0,
  "signals": [],
  "soc_report": [],
  "confidence": 0
}
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
            "soc_report": ["LLM output parsing failed"],
            "confidence": 50
        }

    return {
        **state,
        "reasoning": result,
        "verdict": result.get("verdict", "suspicious"),
        "risk_score": result.get("score", 50)
    }