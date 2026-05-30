from state import AgentState
from tools.url_tool import url_reputation_check


def threat_analysis(state: AgentState):
    iocs = state.get("extracted_iocs", {})
    urls = iocs.get("urls", [])

    results = {}

    for url in urls:
        results[url] = url_reputation_check(url)

    state["threat_data"] = results

    state["investigation_steps"].append(
        "Threat Agent performed URL reputation analysis (clean scope)"
    )

    return state