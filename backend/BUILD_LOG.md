# Build Log

# Project

Agentic SOC Phishing Detection System

# Goal

Build a multi-agent SOC system for phishing detection using structured reasoning and tool-based intelligence.

# Timeline

## Phase 1 — Core Setup

- FastAPI backend
- React frontend
- LangGraph workflow

Files:
main.py
runtime_graph.py
state.py

## Phase 2 — IOC Extraction

- URL extraction
- Domain extraction

ioc_agent.py

## Phase 3 — Threat Intelligence

- URL reputation checks
- Tool abstraction

threat_agent.py
tools/url_tool.py
tools/tool_registry.py

## Phase 4 — Memory System

- Incident history
- Pattern matching

memory_agent.py
memory/incident_memory.json

## Phase 5 — Risk Engine

- Risk scoring (0–100)
- SOC reasoning

reasoning_agent.py

## Phase 6 — Reporting

- Final SOC classification
- JSON output

reporting_agent.py

# Workflow

ioc
↓
threat
↓
memory
↓
reasoning
↓
report

workflow = StateGraph(AgentState)

workflow.add_node("ioc", extract_iocs)
workflow.add_node("threat", threat_analysis)
workflow.add_node("memory", memory_agent)
workflow.add_node("reasoning", reasoning_agent)
workflow.add_node("report", reporting_agent)

workflow.set_entry_point("ioc")

workflow.add_edge("ioc", "threat")
workflow.add_edge("threat", "memory")
workflow.add_edge("memory", "reasoning")
workflow.add_edge("reasoning", "report")

app = workflow.compile()

# Evaluation

- Dataset: 400 samples
- Phishing: 150
- Legit: 150
- Edge: 100

# Outcome

Multi-agent SOC system with explainable phishing detection and structured reasoning.