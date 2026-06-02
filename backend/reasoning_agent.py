import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def reasoning_agent(state):

    email = state.get("email", "")
    iocs = state.get("iocs", {})
    threat = state.get("threat", {})
    memory = state.get("memory", {})

    base_score = threat.get("base_score", 0)
    memory_score = memory.get("memory_score", 0)

    # FINAL SCORE (important fix)
    score = min(base_score + memory_score, 100)

    prompt = f"""
You are a SENIOR SOC ANALYST.

EMAIL:
{email}

IOC FEATURES:
{iocs}

THREAT SIGNALS:
{threat}

MEMORY CONTEXT:
{memory}

Rules:
- Job scams + data harvesting = HIGH RISK
- Gmail recruiters impersonating institutions = SUSPICIOUS
- Multiple signals = escalate severity

Return ONLY JSON:

{{
  "score": {score},
  "verdict": "legit|suspicious|phishing",
  "signals": [],
  "soc_report": []
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": "Strict SOC phishing analyst."},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content.strip()
    content = content.replace("```json", "").replace("```", "")

    try:
        result = json.loads(content)
    except:
        result = {
            "score": score,
            "verdict": "suspicious",
            "signals": ["fallback_triggered"],
            "soc_report": ["LLM parsing failed, fallback used"]
        }

    return {
        **state,
        "reasoning": result,
        "verdict": result["verdict"],
        "risk_score": result["score"]
    }