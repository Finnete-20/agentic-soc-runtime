from state import AgentState


def reporting_agent(state: AgentState):
    risk = state["risk_score"]

    # SOC-style classification thresholds
    if risk >= 70:
        verdict = "phishing"
    elif risk >= 40:
        verdict = "suspicious"
    else:
        verdict = "legit"

    state["final_report"] = {
        "verdict": verdict,
        "risk_score": risk,
        "iocs": state["extracted_iocs"],
        "threat_data": state["threat_data"],
        "investigation_steps": state["investigation_steps"]
    }

    state["investigation_steps"].append(
        "Reporting Agent applied SOC classification thresholds"
    )

    return state