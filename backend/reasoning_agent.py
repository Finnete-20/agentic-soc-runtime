from state import AgentState


def reasoning_agent(state: AgentState):

    threat_data = state.get("threat_data", {})
    memory_hits = state.get("memory_matches", [])

    iocs = state.get("extracted_iocs", {})
    urls = iocs.get("urls", [])
    domains = iocs.get("domains", [])

    risk = 0

    # -------------------------
    # URL threat scoring (HIGH SIGNAL)
    # -------------------------
    for url, result in threat_data.items():
        if isinstance(result, dict):
            risk += result.get("risk_score", 0) * 0.7

    # -------------------------
    # Domain risk (MEDIUM SIGNAL)
    # -------------------------
    risk += len(domains) * 5

    # -------------------------
    # URL count risk
    # -------------------------
    risk += len(urls) * 10

    # -------------------------
    # Memory boost (STRONG SIGNAL)
    # -------------------------
    if memory_hits:
        risk += 20
        state["investigation_steps"].append("Memory match → +20 risk boost")

    # clamp
    risk = min(100, risk)

    state["risk_score"] = risk

    state["investigation_steps"].append(
        f"Reasoning Agent computed calibrated risk: {risk}"
    )

    return state