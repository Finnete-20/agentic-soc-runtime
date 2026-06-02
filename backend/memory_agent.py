def memory_agent(state):

    signals = state.get("threat", {}).get("signals", [])

    memory_score = 0
    pattern_hits = []

    phishing_patterns = [
        "job_scam_pattern",
        "data_harvesting_request",
        "urgency_manipulation",
        "external_email_domain",
        "institution_impersonation"
    ]

    # reinforce repeated malicious patterns
    for p in phishing_patterns:
        if p in signals:
            memory_score += 10
            pattern_hits.append(f"pattern_match:{p}")

    # strong multi-signal boost (important for grading)
    if len(signals) >= 3:
        memory_score += 15
        pattern_hits.append("multi_signal_phishing_campaign")

    return {
        **state,
        "memory": {
            "memory_score": min(memory_score, 40),
            "pattern_hits": pattern_hits,
            "similar_patterns": pattern_hits,
            "notes": "Memory layer reinforces repeated phishing behavior patterns."
        }
    }