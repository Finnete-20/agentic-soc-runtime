def reasoning_agent(state):
    base = state["threat"]["base_score"]
    memory = state["memory"]["memory_score"]

    score = base + memory

    if score >= 65:
        verdict = "phishing"
    elif score >= 35:
        verdict = "suspicious"
    else:
        verdict = "legit"

    return {
        **state,
        "risk_score": score,
        "reasoning": {
            "score": score,
            "verdict": verdict
        }
    }