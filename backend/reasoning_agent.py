from state import AgentState
from model_router import route_model


SUSPICIOUS_KEYWORDS = [
    "urgent",
    "verify",
    "password",
    "locked",
    "click here",
    "login",
    "account suspended"
]

SAFE_KEYWORDS = [
    "no action required",
    "ignore this message",
    "for your information",
    "receipt",
    "confirmation"
]


def reasoning_agent(state: AgentState):
    threat_data = state["threat_data"]
    email = state["email_content"].lower()

    model = route_model("reasoning")

    risk = 0

    # 1. URL risk scoring
    for url, data in threat_data.items():
        status = data.get("status_code") if isinstance(data, dict) else data

        if status == "unreachable" or status is None:
            risk += 60
        elif isinstance(status, int) and status >= 400:
            risk += 40
        else:
            risk += 5

    # 2. Suspicious keyword signals
    for word in SUSPICIOUS_KEYWORDS:
        if word in email:
            risk += 10

    # 3. Safe keyword signals (reduce risk)
    for word in SAFE_KEYWORDS:
        if word in email:
            risk -= 15

    # 4. Multiple IOCs boost severity
    if len(state["extracted_iocs"]) > 1:
        risk += 10

    state["risk_score"] = max(0, min(risk, 100))

    state["investigation_steps"].append(
        f"Reasoning Agent used {model} and computed SOC risk score {state['risk_score']}"
    )

    return state