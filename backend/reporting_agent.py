def reporting_agent(state):

    score = state["reasoning"]["score"]

    if score >= 70:
        verdict = "phishing"
    elif score >= 35:
        verdict = "suspicious"
    else:
        verdict = "legit"

    return {
        "verdict": verdict,
        "risk_score": score,
        "signals": state["reasoning"].get("signals", []),
        "soc_report": state["reasoning"].get("soc_report", []),
        "iocs": state["iocs"]
    }