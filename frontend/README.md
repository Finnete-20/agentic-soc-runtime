# Agentic SOC Phishing Detection System

## Overview

The Agentic SOC Phishing Detection System is an AI-powered Security Operations Center (SOC) assistant designed to detect phishing emails using a multi-agent architecture.

The system simulates SOC-style investigation workflows using LangGraph, LLM-driven reasoning, tool-based intelligence, memory reasoning, and structured reporting.

The goal is explainability and structured decision-making rather than only classification accuracy.

---

## Key Features

### Multi-Agent SOC Pipeline

The system uses a structured SOC-style agentic workflow that simulates real security analyst reasoning.

The pipeline is decomposed into five specialized agents:

---

### 1. IOC Agent

Extracts security-relevant artifacts from email content.

It identifies:

- Email addresses
- URLs
- Domains
- Basic suspicious indicators

Purpose:
Build structured intelligence from raw email input.

---

### 2. Threat Agent

Evaluates the extracted indicators and assigns initial threat signals.

It analyzes:

- Impersonation attempts (fake organizations or domains)
- Social engineering patterns
- Urgency manipulation ("act now", "limited time")
- Monetary lure (stipends, rewards, refunds)
- External communication patterns

Purpose:
Model attacker intent and behavioral patterns.

---

### 3. Memory Agent

Maintains lightweight historical context of known attack patterns.

It can match:

- Previously seen phishing patterns
- Repeated scam structures
- Known malicious keywords or themes

Purpose:
Improve detection consistency across repeated attack styles.

---

### 4. Reasoning Agent (LLM-Powered)

Aggregates signals from all previous agents and computes a final risk score.

This node uses an LLM-based SOC analyst to interpret signals, assess context, and produce a structured decision.

It combines:

- IOC signals
- Threat intelligence signals
- Memory matches
- LLM reasoning over full context

Then assigns:

- Risk score (0–100)
- Final classification decision (legit / suspicious / phishing)

Purpose:
Act as the LLM-driven decision engine of the SOC workflow, replacing rule-based classification.

---

### 5. Reporting Agent (LLM-Assisted SOC Output)

Generates the final structured SOC output.

It returns:

- Final verdict (legit / suspicious / phishing)
- Risk score
- Extracted indicators
- Supporting reasoning context

The report is generated in a SOC analyst style using LLM-based summarization of all agent outputs.

Purpose:
Provide explainable SOC-style output for analysts.

---

## Tool-Based Architecture

A modular tool layer is used for threat intelligence simulation.

Capabilities:

- URL reputation checking
- Mock VirusTotal integration (tool-based enrichment)
- Tool abstraction layer
- Extensible SOC tool design

Future integrations:

- VirusTotal API
- AbuseIPDB
- URLScan
- OpenCTI

---

## Memory System

The system maintains historical context:

- Stores past incidents
- Detects repeated malicious patterns
- Improves contextual reasoning
- Enhances risk scoring

---

## Risk Scoring

Risk score range: 0–100

- 0–30 → Legitimate
- 31–60 → Suspicious
- 61–100 → Phishing

---

## Architecture

### System Flow

```text
Email Input
    ↓
IOC Agent
    ↓
Threat Agent
    ↓
Memory Agent
    ↓
Reasoning Agent (LLM)
    ↓
Reporting Agent (LLM)
    ↓
Final Classification Output

LangGraph Workflow

Workflow:

ioc → threat → memory → reasoning → report
```
---
### Implementation:

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

---
### Tech Stack

- Python
- FastAPI
- LangGraph
- OpenAI GPT-4.1-mini (LLM reasoning layer)
- React
- TailwindCSS

---
### How to Run
Backend

cd backend

pip install -r requirements.txt

uvicorn main:api --reload

Frontend

cd frontend

npm install

npm run dev

---

### Evaluation

python evaluate.py

backend/evaluation/evaluation.md

backend/evaluation/data

Evaluation includes:

Accuracy
Precision
Recall
Confusion matrix
Multi-scenario phishing dataset (40 emails including edge cases)

---
### Purpose

This system demonstrates:

- Multi-agent reasoning (LangGraph workflow execution)
- LLM-assisted SOC decision-making
- Tool-based intelligence (mock threat enrichment)
- Memory-enhanced detection
- Explainable phishing detection
- Real evaluation using labeled datasets