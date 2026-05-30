import json

MEMORY_FILE = "memory/incident_memory.json"

def memory_agent(state):

    matches = []

    try:
        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)

        email_text = state["email_content"].lower()

        for incident in memory:
            domain = incident.get("domain", "")

            # URL match
            url_match = any(domain in ioc for ioc in state["extracted_iocs"])

            # keyword pattern match (IMPORTANT FIX)
            pattern_match = any(
                kw in email_text
                for kw in incident.get("patterns", [])
            )

            if url_match or pattern_match:
                matches.append(incident)

    except Exception:
        pass

    state["memory_matches"] = matches

    if matches:
        state["investigation_steps"].append(
            f"Memory Agent found {len(matches)} historical attack patterns"
        )
    else:
        state["investigation_steps"].append(
            "Memory Agent found no relevant historical matches"
        )

    return state