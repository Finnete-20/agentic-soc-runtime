def reasoning_agent(state):
    base = state["threat"]["base_score"]
    memory_bonus = state["memory"]["memory_score"]

    score = base + memory_bonus

    if score > 60:
        verdict = "phishing"
    elif score > 30:
        verdict = "suspicious"
    else:
        verdict = "legit"

    return {
        **state,
        "reasoning": {
            "score": score,
            "verdict": verdict
        }
    }