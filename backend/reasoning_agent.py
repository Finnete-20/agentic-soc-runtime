from openai import OpenAI
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def reasoning_agent(state):
    """
    SOC ANALYST LLM (GUIDED, NOT RULE-BASED)

    IMPORTANT:
    - No hardcoded thresholds
    - No if/else logic
    - BUT structured signal interpretation is allowed
    """

    email = state.get("email", "")
    iocs = state.get("iocs", {})
    threat = state.get("threat", {})
    virustotal = state.get("virustotal", [])
    memory = state.get("memory", {})

    # We do NOT classify — we only provide structured context
    # This prevents LLM drift while keeping it non-rule-based

    structured_context = {
        "ioc_signals": iocs.get("features", {}),
        "threat_signals": threat.get("signals", []),
        "virustotal_summary": virustotal,
        "memory_signals": memory.get("pattern_hits", [])
    }

    prompt = f"""
You are a senior SOC analyst in a Security Operations Center.

You must analyze emails and determine risk.

IMPORTANT RULES:
- Do NOT use fixed thresholds or if/else logic
- Do NOT blindly label everything as phishing
- Use reasoning grounded in signals
- Balance false positives and false negatives like a real analyst

---

EMAIL:
{email}

---

STRUCTURED SECURITY SIGNALS:
{json.dumps(structured_context, indent=2)}

---

TASK:
1. Analyze all signals holistically
2. Identify attack intent if present
3. Consider false positives (e.g., benign university emails, internal systems)
4. Assign a realistic SOC risk score (0–100)
5. Choose one:
   - legit
   - suspicious
   - phishing

---

CLASSIFICATION GUIDELINES (NOT RULES):
- phishing → strong intent + multiple aligned signals
- suspicious → mixed signals or weak intent
- legit → no meaningful malicious indicators

---

RETURN STRICT JSON ONLY:

{{
  "verdict": "legit | suspicious | phishing",
  "risk_score": number,
  "confidence": number,
  "signals": ["key contributing factors"],
  "soc_report": [
    "SOC reasoning line 1",
    "SOC reasoning line 2",
    "SOC reasoning line 3"
  ]
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert SOC analyst. You are careful, balanced, and avoid over-flagging."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )

    content = response.choices[0].message.content.strip()

    try:
        result = json.loads(content)
    except Exception:
        result = {
            "verdict": "suspicious",
            "risk_score": 50,
            "confidence": 50,
            "signals": ["parse_error"],
            "soc_report": [content]
        }

    state["reasoning"] = result
    state["verdict"] = result["verdict"]
    state["risk_score"] = result["risk_score"]

    return state