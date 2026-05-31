def reporting_agent(state):
    return {
        "verdict": state["reasoning"]["verdict"],
        "risk_score": state["reasoning"]["score"],
        "iocs": state["iocs"],
        "threat_data": state["threat"],
        "memory": state["memory"],
        "reasoning": state["reasoning"]
    }