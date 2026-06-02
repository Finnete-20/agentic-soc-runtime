def threat_analysis(state):

    text = state.get("email", "").lower()

    score = 0
    signals = []

    # -----------------------------
    # JOB SCAM DETECTION (CRITICAL)
    # -----------------------------
    job_keywords = [
        "remote student worker",
        "student worker",
        "job",
        "employment",
        "position",
        "hiring",
        "opportunity",
        "work from home",
        "remote work"
    ]

    if any(k in text for k in job_keywords):
        score += 30
        signals.append("job_scam_pattern")

    # -----------------------------
    # DATA HARVESTING (VERY STRONG SIGNAL)
    # -----------------------------
    data_keywords = [
        "phone number",
        "full name",
        "personal email",
        "send your details",
        "contact information",
        "email address"
    ]

    if any(k in text for k in data_keywords):
        score += 30
        signals.append("data_harvesting_request")

    # -----------------------------
    # INSTITUTION IMPERSONATION
    # -----------------------------
    institution_keywords = [
        "department",
        "university",
        "college",
        "office",
        "academic"
    ]

    if any(k in text for k in institution_keywords):
        score += 15
        signals.append("institution_impersonation")

    # -----------------------------
    # EXTERNAL GMAIL SENDER
    # -----------------------------
    if "@gmail.com" in text:
        score += 10
        signals.append("external_email_domain")

    # -----------------------------
    # URGENCY / PRESSURE LANGUAGE
    # -----------------------------
    urgency_keywords = [
        "urgent",
        "immediately",
        "apply now",
        "limited",
        "expires soon"
    ]

    if any(k in text for k in urgency_keywords):
        score += 10
        signals.append("urgency_manipulation")

    # -----------------------------
    # FINAL NORMALIZATION
    # -----------------------------
    score = min(score, 100)

    return {
        **state,
        "threat": {
            "base_score": score,
            "signals": signals
        }
    }