from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def reasoning_agent(state):
    """
    PURE LLM-DRIVEN SOC ANALYST
    No rules. No scoring logic. No thresholds.
    """

    email = state.get("email", "")
    iocs = state.get("iocs", {})
    threat = state.get("threat", {})
    virustotal = state.get("virustotal", [])
    memory = state.get("memory", {})

    prompt = f"""
You are a senior SOC analyst working in a Security Operations Center.

Your job is to analyze emails for phishing risk.

You are NOT allowed to use fixed rules or scoring systems.
You must reason like a human analyst.

---

EMAIL:
{email}

---

IOC EXTRACTION:
{json.dumps(iocs, indent=2)}

---

THREAT ANALYSIS:
{json.dumps(threat, indent=2)}

---

VIRUSTOTAL RESULTS:
{json.dumps(virustotal, indent=2)}

---

MEMORY CONTEXT:
{json.dumps(memory, indent=2)}

---

INSTRUCTIONS:
- Decide if the email is: legit, suspicious, or phishing
- Use reasoning, not rules
- Consider context, intent, and subtle signals
- VirusTotal may be misleading (do not blindly trust it)
- Explain like a SOC analyst writing an incident report
- Assign a risk score (0–100) based on judgment, not formula

---

RETURN ONLY VALID JSON:

{{
  "verdict": "legit | suspicious | phishing",
  "risk_score": number,
  "confidence": number,
  "signals": ["list of key indicators you used"],
  "soc_report": [
    "SOC-style explanation line 1",
    "SOC-style explanation line 2",
    "SOC-style explanation line 3"
  ]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a highly experienced SOC analyst specializing in phishing detection."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content.strip()

    try:
        result = json.loads(content)
    except Exception:
        # fallback safe parse (DO NOT use rules, just fail gracefully)
        result = {
            "verdict": "suspicious",
            "risk_score": 50,
            "confidence": 50,
            "signals": ["llm_parse_error"],
            "soc_report": [content]
        }

    state["reasoning"] = result
    state["verdict"] = result["verdict"]
    state["risk_score"] = result["risk_score"]

    return state