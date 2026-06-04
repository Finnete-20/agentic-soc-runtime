from langgraph.graph import StateGraph
from state import AgentState

from ioc_agent import extract_iocs
from threat_agent import threat_analysis
from memory_agent import memory_agent
from reasoning_agent import reasoning_agent
from reporting_agent import reporting_agent
from virustotal_agent import virustotal_agent  # ✅ FIXED

# ✅ FIX: make sure this exists in virustotal_agent.py
from virustotal_agent import virustotal_agent


# -----------------------------
# BUILD LANGGRAPH WORKFLOW
# -----------------------------

workflow = StateGraph(AgentState)

# Nodes
workflow.add_node("ioc", extract_iocs)
workflow.add_node("threat", threat_analysis)
workflow.add_node("memory", memory_agent)

# 🔥 VirusTotal inserted AFTER IOC for enrichment
workflow.add_node("virustotal", virustotal_agent)

workflow.add_node("reasoning", reasoning_agent)
workflow.add_node("report", reporting_agent)

# Entry point
workflow.set_entry_point("ioc")

# Flow (IMPORTANT ORDER)
workflow.add_edge("ioc", "threat")
workflow.add_edge("threat", "memory")

# 🔥 VirusTotal step (new intelligence layer)
workflow.add_edge("memory", "virustotal")

workflow.add_edge("virustotal", "reasoning")
workflow.add_edge("reasoning", "report")

# Compile app
app = workflow.compile()