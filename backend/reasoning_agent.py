def reasoning_agent(state):
    base = state["threat"]["base_score"]

    memory_bonus = state["memory"].get(
        "memory_score",
        0
    )

    score = base + memory_bonus

    score = min(score, 100)

    if score >= 70:
        verdict = "phishing"
    elif score >= 35:
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