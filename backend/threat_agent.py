from state import AgentState
from tools.url_tool import url_reputation_check


def threat_analysis(state: AgentState):
    urls = state["extracted_iocs"]

    results = {}

    for url in urls:
        results[url] = url_reputation_check(url)

    state["threat_data"] = results

    state["investigation_steps"].append(
        "Threat Agent used MCP-style tool registry for URL analysis"
    )

    return state