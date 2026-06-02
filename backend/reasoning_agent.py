import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def reasoning_agent(state):

    prompt = f"""
You are a SENIOR SOC ANALYST.

IMPORTANT SECURITY RULES:
- Job recruitment emails asking for personal data are HIGHLY LIKELY PHISHING
- Gmail recruiters pretending to represent institutions are suspicious
- Requests for phone/email/name collection are data harvesting
- Treat unsolicited job offers as suspicious by default

Now analyze:

EMAIL:
{state.get("email")}

IOC FEATURES:
{state.get("iocs")}

THREAT:
{state.get("threat")}

Return JSON ONLY:

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
            {"role": "system", "content": "You are a strict SOC phishing classifier."},
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