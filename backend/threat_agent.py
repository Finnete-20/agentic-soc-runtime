def threat_analysis(state):
    iocs = state["iocs"]
    text = state["email"].lower()

    keyword_hits = [
        k for k in ["urgent", "verify", "password", "login", "account", "suspended"]
        if k in text
    ]

    score = (
        iocs["url_count"] * 25 +
        iocs["suspicious_words"] * 15 +
        len(keyword_hits) * 10
    )

    score = min(score, 100)

    return {
        **state,
        "threat": {
            "base_score": score,
            "keyword_hits": keyword_hits
        }
    }