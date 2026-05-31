from langgraph.graph import StateGraph, END
from state import AgentState

from ioc_agent import extract_iocs
from reasoning_agent import reason_about_email
from threat_agent import score_threat
from memory_agent import store_memory

def ioc_node(state):
    state["iocs"] = extract_iocs(state["email"])
    return state

def reasoning_node(state):
    state["reasoning"] = reason_about_email(state)
    return state

def threat_node(state):
    state["result"] = score_threat(state)
    return state

def memory_node(state):
    store_memory(state)
    return state["result"]

graph = StateGraph(AgentState)

graph.add_node("ioc", ioc_node)
graph.add_node("reasoning", reasoning_node)
graph.add_node("threat", threat_node)
graph.add_node("memory", memory_node)

graph.set_entry_point("ioc")

graph.add_edge("ioc", "reasoning")
graph.add_edge("reasoning", "threat")
graph.add_edge("threat", "memory")
graph.add_edge("memory", END)

app = graph.compile()