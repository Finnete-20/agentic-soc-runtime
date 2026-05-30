import json

MEMORY_FILE = "memory/incident_memory.json"

def memory_agent(state):

    matches = []

    try:

        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)

        for ioc in state["extracted_iocs"]:

            for incident in memory:

                if incident["domain"] in ioc:
                    matches.append(incident)

    except Exception:
        pass

    state["memory_matches"] = matches

    state["investigation_steps"].append(
        f"Memory Agent searched {len(matches)} historical incidents"
    )

    return state