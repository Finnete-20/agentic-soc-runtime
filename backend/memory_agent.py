import json

MEMORY_FILE = "memory/incident_memory.json"


def memory_agent(state):

    matches = []

    try:
        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)

        for item in state.get("extracted_iocs", []):

            for incident in memory:

                domain = incident.get("domain", "")

                if domain and domain in str(item):
                    matches.append(incident)

    except Exception:
        pass

    state["memory_matches"] = matches

    state["investigation_steps"].append(
        f"Memory Agent → {len(matches)} matches found"
    )

    return state