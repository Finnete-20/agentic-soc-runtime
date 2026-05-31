def threat_analysis(state):
    text = state["email"].lower()
    iocs = state["iocs"]

    keyword_hits = [
        k for k in ["urgent", "verify", "password", "login", "account",
                    "apply", "internship", "selected", "offer", "limited"]
        if k in text
    ]

    # 🚨 NEW: EMAIL DOMAIN RISK
    email_risk = len(iocs.get("emails", [])) * 10

    # 🚨 NEW: SOCIAL ENGINEERING SIGNALS
    social_signals = 0
    if "apply" in text and "student" in text:
        social_signals += 15
    if "stipend" in text or "$" in text:
        social_signals += 20
    if "first-come" in text:
        social_signals += 10

    score = (
        iocs["url_count"] * 25 +
        iocs["suspicious_words"] * 15 +
        len(keyword_hits) * 8 +
        email_risk +
        social_signals
    )

    score = min(score, 100)

    return {
        **state,
        "threat": {
            "base_score": score,
            "keyword_hits": keyword_hits
        }
    }