from langgraph.graph import StateGraph, END
from state import AgentState

from ioc_agent import extract_iocs
from reasoning_agent import reason_about_email
from threat_agent import score_threat

def ioc_node(state):
    state["iocs"] = extract_iocs(state["email"])
    return state

def reasoning_node(state):
    state["reasoning"] = reason_about_email(state)
    return state

def threat_node(state):
    result = score_threat(state)

    state["verdict"] = result["verdict"]
    state["risk_score"] = result["risk_score"]
    state["iocs"] = result["iocs"]
    state["reasoning"] = result["reasoning"]

    return state

graph = StateGraph(AgentState)

graph.add_node("ioc", ioc_node)
graph.add_node("reasoning", reasoning_node)
graph.add_node("threat", threat_node)

graph.set_entry_point("ioc")

graph.add_edge("ioc", "reasoning")
graph.add_edge("reasoning", "threat")
graph.add_edge("threat", END)

app = graph.compile()