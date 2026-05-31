def score_threat(state):
    iocs = state["iocs"]
    reasoning = state.get("reasoning", {})

    score = 0

    # URL risk
    score += iocs["url_count"] * 20

    # keyword risk
    score += iocs["suspicious_words"] * 25

    # uppercase spam
    score += int(iocs["uppercase_ratio"] * 20)

    # reasoning boost
    if len(reasoning.get("reasons", [])) >= 2:
        score += 10

    score = min(score, 100)

    if score >= 70:
        verdict = "malicious"
    elif score >= 40:
        verdict = "suspicious"
    else:
        verdict = "safe"

    return {
        "verdict": verdict,
        "risk_score": score,
        "iocs": iocs,
        "reasoning": reasoning
    }