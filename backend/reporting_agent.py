def reporting_agent(state):
    return {
        "verdict": state["reasoning"]["verdict"],
        "risk_score": state["reasoning"]["score"],
        "iocs": state["iocs"],
        "memory": state["memory"],
        "threat": state["threat"],
        "reasoning": state["reasoning"]
    }