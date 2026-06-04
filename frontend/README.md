# Agentic SOC Phishing Detection System

## Overview

The Agentic SOC Phishing Detection System is an AI-powered Security Operations Center (SOC) assistant designed to detect phishing emails using a multi-agent architecture.

The system simulates real SOC investigation workflows using LangGraph, LLM-driven reasoning, real-time threat intelligence (VirusTotal API), memory-based reasoning, and structured reporting.

The goal is explainability, structured decision-making, and SOC-style reasoning rather than only classification accuracy.

---

## Key Features

### Multi-Agent SOC Pipeline

The system uses a structured SOC-style workflow that simulates real security analyst reasoning.

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

Evaluates extracted indicators and assigns initial threat signals.

It analyzes:

- Impersonation attempts (fake organizations or domains)
- Social engineering patterns
- Urgency manipulation ("act now", "limited time")
- External email domains
- Data harvesting indicators (Google Forms, surveys)

Purpose:
Model attacker intent and behavioral patterns.

---

### 3. VirusTotal Agent (Threat Intelligence Layer)

Performs real-time URL reputation analysis using the VirusTotal API.

It provides:

- Malicious score
- Suspicious score
- Harmless score
- Undetected classification

Purpose:
Validate extracted URLs using external threat intelligence sources.

---

### 4. Memory Agent

Maintains lightweight historical context of known attack patterns.

It can match:

- Previously seen phishing patterns
- Repeated scam structures
- Known malicious domains and behaviors

Purpose:
Improve detection consistency across repeated attack styles.

---

### 5. Reasoning Agent (LLM-Powered SOC Analyst)

Aggregates signals from all previous agents and computes final classification.

This node uses an LLM (GPT-4.1-mini) to interpret:

- IOC signals
- Threat intelligence results
- VirusTotal API outputs
- Memory matches

It produces:

- Risk score (0–100)
- Final classification (legit / suspicious / phishing)
- Structured SOC reasoning

Purpose:
Act as an AI SOC analyst replacing rule-based classification.

---

### 6. Reporting Agent

Generates final SOC-style structured output.

It returns:

- Final verdict
- Risk score
- Extracted indicators
- SOC explanation summary

Purpose:
Provide explainable security output for analysts.

---

## Tool-Based Architecture

A modular tool layer is used for threat intelligence enrichment.

Capabilities:

- URL reputation checking
- Real VirusTotal API integration
- Tool abstraction layer
- Extensible SOC intelligence design

Future integrations:

- AbuseIPDB
- URLScan.io
- OpenCTI

---

## Memory System

The system maintains historical security context:

- Stores known phishing patterns
- Detects repeated attack structures
- Improves contextual reasoning
- Enhances consistency in risk scoring

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
VirusTotal Agent
    ↓
Memory Agent
    ↓
Reasoning Agent (LLM)
    ↓
Reporting Agent
    ↓
Final Classification Output
```
---
### LangGraph Workflow

workflow = StateGraph(AgentState)

workflow.add_node("ioc", extract_iocs)
workflow.add_node("threat", threat_analysis)
workflow.add_node("virustotal", virustotal_agent)
workflow.add_node("memory", memory_agent)
workflow.add_node("reasoning", reasoning_agent)
workflow.add_node("report", reporting_agent)

workflow.set_entry_point("ioc")

workflow.add_edge("ioc", "threat")
workflow.add_edge("threat", "virustotal")
workflow.add_edge("virustotal", "memory")
workflow.add_edge("memory", "reasoning")
workflow.add_edge("reasoning", "report")

app = workflow.compile()
---
### Tech Stack
- Python
- FastAPI
- LangGraph
- OpenAI GPT-4.1-mini (LLM reasoning layer)
- VirusTotal API (real-time threat intelligence)
- React
- TailwindCSS
---
### How to Run
- Backend
cd backend
pip install -r requirements.txt
uvicorn main:api --reload
- Frontend
cd frontend
npm install
npm run dev
---
### Evaluation

Run evaluation pipeline:

python evaluate.py

- Outputs:

evaluation_result.json
evaluation_report.json
SOC metrics (accuracy, precision, recall)
Confusion matrix
---
### Dataset

Location:

backend/soc_dataset.py

Includes:

Phishing emails
Legitimate emails
Edge-case phishing (Google Forms, spoofing, HR scams)

Total samples: ~40
---

### Purpose

This system demonstrates:

- Multi-agent SOC reasoning (LangGraph workflow execution)
- LLM-assisted security decision-making
- Real-time threat intelligence integration (VirusTotal API)
- Memory-enhanced detection system
- Explainable phishing detection
- Evaluation-driven AI security system
