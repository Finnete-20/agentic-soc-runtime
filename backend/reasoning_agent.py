from state import AgentState


def reasoning_agent(state: AgentState):

    risk = 0

    for item in state.get("threat_data", {}).values():
        risk += item["risk_score"]

    signals = state.get("extracted_iocs", [])

    # nonlinear amplification (THIS IS KEY DIFFERENCE)

    if any(s[0] == "uppercase_ratio" for s in signals):
        risk *= 1.2

    if any(s[0] == "url_count" for s in signals):
        risk += 15

    if any(s[0] == "exclamation_count" for s in signals):
        risk += 10

    # clamp
    risk = min(100, risk)

    state["risk_score"] = risk

    return state