from state import AgentState


def reasoning_agent(state: AgentState):

    threat_data = state.get("threat_data", {})
    memory_hits = state.get("memory_matches", [])

    risk = 0

    # -------------------------
    # Threat intelligence scoring
    # -------------------------
    for url, result in threat_data.items():
        # ensure safe extraction
        if isinstance(result, dict):
            risk += result.get("risk_score", 0)

    # -------------------------
    # Memory boost (VERY IMPORTANT)
    # -------------------------
    if memory_hits:
        risk += 25
        state["investigation_steps"].append(
            "Memory match found → +25 risk boost"
        )

    # -------------------------
    # IOC heuristic boost
    # -------------------------
    if state["extracted_iocs"]:
        risk += len(state["extracted_iocs"]) * 5

    # clamp risk
    risk = min(100, risk)

    state["risk_score"] = risk

    state["investigation_steps"].append(
        f"Reasoning Agent computed final risk: {risk}"
    )

    return state