def threat_analysis(state):
    text = state["email"]
    iocs = state["iocs"]

    keywords = ["urgent", "verify", "password", "login", "account", "suspended"]

    hits = [k for k in keywords if k in text.lower()]

    score = len(hits) * 10 + iocs["url_count"] * 20

    return {
        **state,
        "threat": {
            "keyword_hits": hits,
            "base_score": score
        }
    }