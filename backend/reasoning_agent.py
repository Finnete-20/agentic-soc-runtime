def reasoning_agent(state):
    threat = state.get("threat", {})
    memory = state.get("memory", {})

    base_score = threat.get("base_score", 0)
    memory_score = memory.get("memory_score", 0)

    score = min(base_score + memory_score, 100)

    signals = threat.get("signals", [])
    soc_report = []

    # Explain suspicious indicators
    if "external_email_domain" in signals:
        soc_report.append(
            "Sender uses an external email domain rather than an institutional domain"
        )

    if "google_forms_link" in signals:
        soc_report.append(
            "Email contains a Google Forms link frequently used in phishing campaigns"
        )

    if "institution_impersonation" in signals:
        soc_report.append(
            "Message claims association with an educational or organizational institution"
        )

    if "bulk_recipients" in signals:
        soc_report.append(
            "Message appears distributed to multiple recipients"
        )

    if "urgency_manipulation" in signals:
        soc_report.append(
            "Language attempts to create urgency or pressure immediate action"
        )

    if "credential_harvesting" in signals:
        soc_report.append(
            "Email requests account verification or credential submission"
        )

    if "monetary_lure" in signals:
        soc_report.append(
            "Financial incentive or payment offer detected"
        )

    if "contains_link" in signals:
        soc_report.append(
            "Email contains an external hyperlink"
        )

    # Determine verdict
    if score >= 61:
        verdict = "phishing"
    elif score >= 31:
        verdict = "suspicious"
    else:
        verdict = "legit"

    # Legitimate email explanations
    if verdict == "legit" and len(soc_report) == 0:
        soc_report = [
            "No credential harvesting indicators detected",
            "No suspicious links detected",
            "No urgency manipulation detected",
            "No impersonation indicators detected",
            "Message appears consistent with legitimate business communication"
        ]

    return {
        **state,
        "reasoning": {
            "score": score,
            "verdict": verdict,
            "signals": signals,
            "soc_report": soc_report
        }
    }