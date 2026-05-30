from state import AgentState


def reasoning_agent(state: AgentState):

    threat_data = state.get("threat_data", {})
    memory_hits = state.get("memory_matches", [])
    signals = state.get("phishing_signals", [])

    risk = 0

    # -------------------------
    # URL threat intelligence
    # -------------------------
    for url, result in threat_data.items():
        if isinstance(result, dict):
            # reachable phishing domains = strong signal
            if result.get("reachable"):
                risk += 30
            else:
                risk += 10

    # -------------------------
    # MEMORY SIGNAL (adaptive boost)
    # -------------------------
    if memory_hits:
        risk += min(30, len(memory_hits) * 15)

    # -------------------------
    # IOC URL presence
    # -------------------------
    risk += len(state.get("extracted_iocs", [])) * 20

    # -------------------------
    # PHISHING LANGUAGE SIGNALS (IMPORTANT FIX)
    # -------------------------
    risk += len(signals) * 6

    # -------------------------
    # clamp
    # -------------------------
    risk = max(0, min(100, risk))

    state["risk_score"] = risk

    state["investigation_steps"].append(
        f"Reasoning Agent computed calibrated risk: {risk}"
    )

    return state