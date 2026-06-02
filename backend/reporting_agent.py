def reporting_agent(state):

    r = state.get("reasoning", {})

    return {
        "verdict": r.get("verdict", "unknown"),
        "risk_score": r.get("score", 0),
        "signals": r.get("signals", []),
        "soc_report": r.get("soc_report", []),
        "iocs": state.get("iocs", {}),
        "virustotal": state.get("virustotal", [])
    }