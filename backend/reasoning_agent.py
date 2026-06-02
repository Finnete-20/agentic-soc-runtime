import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def reasoning_agent(state):

    prompt = f"""
You are the FINAL SOC decision engine.

Use ALL data to classify the email.

IOC:
{state.get("iocs")}

Threat:
{state.get("threat")}

Memory:
{state.get("memory")}

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
            {"role": "system", "content": "Final SOC decision engine."},
            {"role": "user", "content": prompt}
        ]
    )

    result = json.loads(response.choices[0].message.content)

    return {
        **state,
        "reasoning": result,
        "verdict": result["verdict"],
        "risk_score": result["score"]
    }