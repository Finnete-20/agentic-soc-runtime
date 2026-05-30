from state import AgentState


def reporting_agent(state: AgentState):
    risk = state["risk_score"]

    if risk >= 65:
        verdict = "phishing"
    elif risk >= 35:
        verdict = "suspicious"
    else:
        verdict = "legit"

    state["final_report"] = {
        "verdict": verdict,
        "risk_score": risk,
        "iocs": state.get("extracted_iocs", {}),
        "threat_data": state.get("threat_data", {}),
        "investigation_steps": state.get("investigation_steps", [])
    }

    state["investigation_steps"].append(
        "Reporting Agent applied calibrated SOC thresholds"
    )

    return state