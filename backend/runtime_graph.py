from langgraph.graph import StateGraph, END
from state import AgentState

from ioc_agent import extract_iocs
from virustotal_agent import virustotal_agent
from threat_agent import threat_analysis
from memory_agent import memory_agent
from reasoning_agent import reasoning_agent
from reporting_agent import reporting_agent
from critique_agent import critique_agent


workflow = StateGraph(AgentState)

# nodes
workflow.add_node("ioc", extract_iocs)
workflow.add_node("virustotal", virustotal_agent)
workflow.add_node("threat", threat_analysis)
workflow.add_node("memory", memory_agent)
workflow.add_node("reasoning", reasoning_agent)
workflow.add_node("critique", critique_agent)
workflow.add_node("report", reporting_agent)

# flow
workflow.set_entry_point("ioc")

workflow.add_edge("ioc", "virustotal")
workflow.add_edge("virustotal", "threat")
workflow.add_edge("threat", "memory")
workflow.add_edge("memory", "reasoning")

# 🔥 LOOP (real agent behavior)
workflow.add_edge("reasoning", "critique")

def route_after_critique(state):
    decision = state.get("critique", {}).get("decision", "approve")

    if decision == "revise":
        return "reasoning"   # loop back
    return "report"

workflow.add_conditional_edges(
    "critique",
    route_after_critique,
    {
        "reasoning": "reasoning",
        "report": "report"
    }
)

workflow.add_edge("report", END)

app = workflow.compile()