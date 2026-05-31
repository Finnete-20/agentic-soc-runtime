def reason_about_email(state):

    email = state["email"]
    iocs = state["iocs"]

    reasons = []

    if iocs["url_count"] > 0:
        reasons.append("Contains external links")

    if iocs["suspicious_words"] > 0:
        reasons.append("Contains phishing keywords")

    if "microsoft" in email.lower():
        reasons.append("Possible brand impersonation")

    return {
        "reasons": reasons
    }