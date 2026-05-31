def reasoning_agent(state):

    email = state["email"].lower()

    signals = []
    soc_report = []

    score = state["threat"]["base_score"]

    if "forms.gle" in email:
        signals.append("google_forms_link")
        soc_report.append("Google Forms link detected")
        score += 15

    if "@gmail.com" in email:
        signals.append("external_email_domain")
        soc_report.append("Sender uses external Gmail account")
        score += 10

    if "gvsu" in email or "grand valley" in email:
        signals.append("institution_impersonation")
        soc_report.append(
            "Email claims association with Grand Valley State University"
        )
        score += 15

    recipient_count = email.count(",")

    if recipient_count > 10:
        signals.append("bulk_recipients")
        soc_report.append(
            "Message appears distributed to many recipients"
        )
        score += 10

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
            "verdict": verdict,
            "signals": signals,
            "soc_report": soc_report
        }
    }