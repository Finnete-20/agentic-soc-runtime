from state import AgentState


def reporting_agent(state: AgentState):

    risk = state["risk_score"]

    # FIXED SOC THRESHOLDS
    if risk >= 60:
        verdict = "phishing"
    elif risk >= 30:
        verdict = "suspicious"
    else:
        verdict = "legit"

    state["final_report"] = {
        "verdict": verdict,
        "risk_score": risk,
        "iocs": state.get("extracted_iocs", []),
        "signals": state.get("phishing_signals", []),
        "threat_data": state.get("threat_data", {}),
        "memory_hits": len(state.get("memory_matches", [])),
        "investigation_steps": state["investigation_steps"]
    }

    state["investigation_steps"].append(
        "Reporting Agent applied calibrated SOC thresholds"
    )

    return state