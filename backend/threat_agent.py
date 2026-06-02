import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def threat_analysis(state):

    prompt = f"""
You are a SOC Threat Analyst.

Analyze phishing signals from IOC data.

IOC:
{state.get("iocs")}

Return JSON:
{{
  "signals": [],
  "base_score": 0,
  "explanation": ""
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": "SOC threat analyst."},
            {"role": "user", "content": prompt}
        ]
    )

    result = json.loads(response.choices[0].message.content)

    return {
        **state,
        "threat": result
    }