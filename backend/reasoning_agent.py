import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def reasoning_agent(state):

    prompt = f"""
You are a Senior SOC Analyst.

Analyze this phishing investigation:

EMAIL:
{state.get("email")}

IOC:
{state.get("iocs")}

THREAT:
{state.get("threat")}

VIRUSTOTAL:
{state.get("virustotal")}

Return ONLY JSON:

{{
  "score": 0-100,
  "verdict": "legit|suspicious|phishing",
  "signals": [],
  "soc_report": []
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a SOC analyst."},
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content

    try:
        result = json.loads(content)
    except:
        result = {
            "score": 50,
            "verdict": "suspicious",
            "signals": ["parse_error"],
            "soc_report": [content]
        }

    return {
        **state,
        "reasoning": result,
        "verdict": result["verdict"],
        "risk_score": result["score"]
    }