def score_threat(state):

    iocs = state["iocs"]
    reasoning = state.get("reasoning", {})

    score = 0

    score += iocs["url_count"] * 25
    score += iocs["suspicious_words"] * 20
    score += int(iocs["uppercase_ratio"] * 30)

    if len(reasoning.get("reasons", [])) >= 2:
        score += 15

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