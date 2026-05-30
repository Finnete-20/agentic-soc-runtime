from state import AgentState
from tools.url_tool import url_reputation_check


def threat_analysis(state: AgentState):
    urls = state["extracted_iocs"]

    results = {}

    for url in urls:
        # only real URLs
        if url.startswith("http"):
            results[url] = url_reputation_check(url)

    state["threat_data"] = results

    state["investigation_steps"].append(
        "Threat Agent analyzed URL reputation signals"
    )

    return state