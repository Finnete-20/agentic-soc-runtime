# Build Log — Agentic SOC Phishing Detection System

---

## Project Overview

This project implements an Agentic Security Operations Center (SOC) system designed to detect phishing emails using a multi-agent architecture.

The system replicates real SOC workflows by breaking down investigation into structured reasoning stages powered by LangGraph.

---

## System Goal

The goal of this system is to:

- Simulate SOC analyst investigation workflows
- Use multi-agent reasoning for phishing detection
- Combine tool-based intelligence and memory
- Produce explainable security decisions
- Support evaluation-driven development

---

## System Architecture Evolution

### Phase 1 — Basic Pipeline

Initial version included:

- Regex-based IOC extraction
- Simple keyword-based scoring
- Rule-based classification

Limitation:
- No modularity
- No reasoning structure
- No evaluation framework

---

### Phase 2 — Multi-Agent Architecture

System was redesigned using LangGraph.

Each function became a specialized agent:

- IOC Extraction Agent
- Threat Intelligence Agent
- Memory Lookup Agent
- Risk Reasoning Engine
- SOC Reporting Agent

This introduced structured decision-making.

---

### Phase 3 — Tool Abstraction Layer

A tool system was added to simulate SOC intelligence sources.

Implemented:

- URL reputation tool
- Tool registry pattern
- Modular intelligence layer

Purpose:

- Decouple tools from agents
- Enable future API integrations
- Improve system scalability

---

### Phase 4 — Memory Integration

A memory layer was added to store historical incidents.

Capabilities:

- Track known malicious domains
- Match recurring attack patterns
- Improve contextual awareness

This improved detection of repeated phishing campaigns.

---

### Phase 5 — Risk Reasoning Engine

The system evolved from rule-based scoring to structured risk reasoning.

Risk score model:

- 0–30 → Legitimate
- 31–60 → Suspicious
- 61–100 → Phishing

The engine aggregates:

- IOC signals
- Threat intelligence results
- Memory matches

---

### Phase 6 — Evaluation Framework

A full evaluation pipeline was introduced.

Features:

- Held-out dataset testing
- Baseline comparison model
- Confusion analysis
- Risk distribution tracking
- Performance reporting

Dataset includes:

- Phishing emails
- Legitimate emails
- Edge-case ambiguous emails

---

## LangGraph Workflow

### Execution Flow

ioc → threat → memory → reasoning → report

---

### Implementation

```python
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
```

### Repository Structure
agentic-soc-runtime/
│
├── backend/
│   ├── main.py
│   ├── runtime_graph.py
│   ├── state.py
│   ├── evaluate.py
│   │
│   ├── ioc_agent.py
│   ├── threat_agent.py
│   ├── memory_agent.py
│   ├── reasoning_agent.py
│   ├── reporting_agent.py
│   │
│   ├── model_router.py
│   │
│   ├── tools/
│   │   ├── tool_registry.py
│   │   └── url_tool.py
│   │
│   ├── memory/
│   │   └── incident_memory.json
│   │
│   └── evaluation/
│       ├── generate_dataset.py
│       ├── evaluation.md
│       ├── evaluation_report.json
│       └── data/
│           ├── phishing_samples.json
│           ├── legit_samples.json
│           └── edge_cases.json
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
│
├── README.md
├── BUILD_LOG.md
└── .gitignore
'''
## SOC workflows are naturally multi-step and require:

decomposition of tasks
traceable reasoning
modular intelligence
Why Tool Abstraction

## Real SOC systems rely on external tools such as:

VirusTotal
AbuseIPDB
URLScan

This system simulates that design pattern.

Why Memory Layer

## Security analysis improves when:

past incidents are reused
patterns are recognized
repeated attacks are tracked