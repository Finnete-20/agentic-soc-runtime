def threat_analysis(state):

    threat_data = {}

    for name, value in state.get("extracted_iocs", []):

        score = 0

        # REAL weighting (continuous signal space)

        if name == "url_count":
            score += value * 35

        elif name == "exclamation_count":
            score += value * 10

        elif name == "uppercase_ratio":
            score += value * 50

        elif name == "suspicious_density":
            score += value * 20

        elif name == "length":
            score += 5 if value < 50 else 0

        elif name == "word_count":
            score += 5 if value < 8 else 0

        threat_data[name] = {"risk_score": score}

    state["threat_data"] = threat_data

    return state