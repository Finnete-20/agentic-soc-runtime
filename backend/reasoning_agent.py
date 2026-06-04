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

    prompt = f"""
You are a SENIOR SOC ANALYST.

Analyze the email using:

IOC DATA:
{iocs}

THREAT SIGNALS:
{threat}

MEMORY PATTERNS:
{memory}

TASK:
1. Decide if phishing / suspicious / legit
2. Explain reasoning clearly
3. Extract signals
4. Provide SOC report bullets

Return STRICT JSON:

{{
  "verdict": "phishing|suspicious|legit",
  "score": 0-100,
  "signals": [],
  "soc_report": [],
  "confidence": 0-100
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=LLM_TEMPERATURE,
        messages=[
            {"role": "system", "content": "You are a SOC analyst AI."},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content.strip()
    content = content.replace("```json", "").replace("```", "")

    try:
        result = json.loads(content)
    except:
        result = {
            "verdict": "suspicious",
            "score": 50,
            "signals": [],
            "soc_report": ["parse fallback"],
            "confidence": 50
        }

    return {
        **state,
        "reasoning": result,
        "verdict": result["verdict"],
        "risk_score": result["score"]
    }