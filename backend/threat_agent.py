import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def threat_analysis(state):

    iocs = state.get("iocs", {}).get("features", {})

    prompt = f"""
You are a SOC Threat Analyst.

Convert these indicators into structured threat intelligence.

Indicators:
{iocs}

Return JSON ONLY:

{{
  "base_score": 0-100,
  "signals": [],
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