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
- Use LLM-driven reasoning for final classification
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
- Mock VirusTotal integration
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
- Support pattern-based scoring consistency

This improved detection of repeated phishing campaigns.

---

### Phase 5 — Risk Reasoning Engine (LLM-Enhanced)

The system evolved from rule-based scoring to structured reasoning enhanced with LLM decision-making.

Risk score model:

- 0–30 → Legitimate
- 31–60 → Suspicious
- 61–100 → Phishing

The engine aggregates:

- IOC signals
- Threat intelligence results
- Memory matches
- LLM-based reasoning over full context

This replaces static classification logic with SOC-style analytical reasoning.

---

### Phase 6 — Evaluation Framework

A full evaluation pipeline was introduced.

Features:

- Held-out dataset testing (20–40 emails)
- Real precision / recall computation
- Confusion matrix analysis
- Edge-case phishing simulation
- Performance reporting via evaluate.py

Dataset includes:

- Phishing emails
- Legitimate emails
- Edge-case ambiguous emails
- Training-simulation emails (false positives tests)

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