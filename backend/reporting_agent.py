import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def reporting_agent(state):

    prompt = f"""
You are a SOC report writer.

Write a professional incident report.

Decision:
{state.get("reasoning")}

IOC:
{state.get("iocs")}

Threat:
{state.get("threat")}

Memory:
{state.get("memory")}

Return JSON:

{{
  "final_report": "...",
  "summary": "...",
  "recommendation": "..."
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": "SOC reporting assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    result = json.loads(response.choices[0].message.content)

    return {
        **state,
        "report": result
    }