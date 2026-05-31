KNOWN_PATTERNS = ["microsoft", "password", "verify"]

def memory_agent(state):
    text = state["email"].lower()

    hits = [p for p in KNOWN_PATTERNS if p in text]

    return {
        **state,
        "memory": {
            "pattern_hits": hits,
            "memory_score": len(hits) * 15
        }
    }