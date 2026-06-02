import os
import json
from openai import OpenAI
from config import LLM_TEMPERATURE

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def reasoning_agent(state):

    email = state.get("email", "")
    threat = state.get("threat", {})
    memory = state.get("memory", {})

    base_score = threat.get("base_score", 0)
    memory_score = memory.get("memory_score", 0)

    score = min(base_score + memory_score, 100)

    prompt = f"""
You are a SENIOR SOC ANALYST.

Return STRICT JSON ONLY.

EMAIL:
{email}

THREAT:
{threat}

MEMORY:
{memory}

Rules:
- Data harvesting + urgency = phishing
- External Gmail + institution mention = suspicious
- Multiple signals = escalate severity

Return format:
{{
  "score": {score},
  "verdict": "legit|suspicious|phishing",
  "signals": [],
  "soc_report": []
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=LLM_TEMPERATURE,
        messages=[
            {"role": "system", "content": "Strict SOC classifier."},
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
            "signals": [],
            "soc_report": ["fallback triggered"]
        }

    return {
        **state,
        "reasoning": result,
        "verdict": result["verdict"],
        "risk_score": result["score"]
    }