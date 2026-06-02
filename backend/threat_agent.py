def threat_analysis(state):

    text = state["email"].lower()

    score = 0
    signals = []

    if any(x in text for x in ["urgent", "immediately", "verify"]):
        score += 20
        signals.append("urgency_manipulation")

    if any(x in text for x in ["password", "login", "verify account"]):
        score += 25
        signals.append("credential_harvesting")

    if "forms.gle" in text:
        score += 10
        signals.append("google_forms_link")

    if "@gmail.com" in text:
        score += 10
        signals.append("external_email_domain")

    return {
        **state,
        "threat": {
            "base_score": score,
            "signals": signals
        }
    }