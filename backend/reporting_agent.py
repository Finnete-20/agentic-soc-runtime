def reporting_agent(state):

    return {
        "verdict": state["reasoning"]["verdict"],
        "risk_score": state["reasoning"]["score"],
        "signals": state["reasoning"].get("signals", []),
        "iocs": state.get("iocs", {})
    }