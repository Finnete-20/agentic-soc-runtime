def threat_analysis(state):
    text = state["email"].lower()

    score = 0
    signals = []

    # impersonation

    institutions = [
        "microsoft",
        "google",
        "paypal",
        "amazon",
        "grand valley",
        "gvsu",
        "office of academic affairs"
    ]

    if any(x in text for x in institutions):
        score += 15
        signals.append("institution_impersonation")

    # urgency

    urgency_words = [
        "urgent",
        "immediately",
        "act now",
        "limited",
        "expires",
        "verify"
    ]

    if any(x in text for x in urgency_words):
        score += 20
        signals.append("urgency_manipulation")

    # credential theft

    credential_words = [
        "password",
        "login",
        "sign in",
        "verify account"
    ]

    if any(x in text for x in credential_words):
        score += 25
        signals.append("credential_harvesting")

    # money lure

    money_words = [
        "$400",
        "weekly stipend",
        "payment",
        "gift card",
        "wire transfer"
    ]

    if any(x in text for x in money_words):
        score += 15
        signals.append("monetary_lure")

    # gmail sender

    if "@gmail.com" in text:
        score += 10
        signals.append("external_email_domain")

    # google forms

    if "forms.gle" in text:
        score += 10
        signals.append("google_forms_link")

    # many recipients

    if text.count(",") > 10:
        score += 10
        signals.append("bulk_recipients")

    return {
        **state,
        "threat": {
            "base_score": score,
            "signals": signals
        }
    }