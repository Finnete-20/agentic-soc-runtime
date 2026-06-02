import os
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def memory_agent(state):

    prompt = f"""
You are a SOC memory system.

Given past patterns and current threat:

THREAT:
{state.get("threat")}

Return:

{{
  "memory_score": 0,
  "similar_patterns": [],
  "notes": ""
}}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": "SOC memory system."},
            {"role": "user", "content": prompt}
        ]
    )

    result = json.loads(response.choices[0].message.content)

    return {
        **state,
        "memory": result
    }