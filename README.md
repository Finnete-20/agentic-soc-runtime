# Agentic SOC Phishing Detection System

## Overview

The Agentic SOC Phishing Detection System is an AI-powered Security Operations Center (SOC) assistant designed to detect phishing emails using a multi-agent architecture.

The system simulates real SOC investigation workflows using LangGraph, LLM-driven reasoning, real-time threat intelligence (VirusTotal API), memory-based reasoning, and structured reporting.

The goal is explainability, structured decision-making, and SOC-style reasoning rather than only classification accuracy.

---

## Key Features

## Multi-Agent SOC Pipeline

The system uses a structured SOC-style workflow that simulates real security analyst reasoning.

The pipeline is decomposed into specialized agents:

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
- Impersonation attempts
- Social engineering patterns
- Urgency manipulation
- External email domains
- Data harvesting indicators

Purpose:
Model attacker intent and behavioral patterns.

---

### 3. VirusTotal Agent

Performs real-time URL reputation analysis using VirusTotal API.

It provides:
- Malicious score
- Suspicious score
- Harmless score
- Undetected classification

Purpose:
Validate extracted URLs using external threat intelligence.

---

### 4. Memory Agent

Maintains historical context of known attack patterns.

It can match:
- Previously seen phishing patterns
- Repeated scam structures
- Known malicious domains

Purpose:
Improve detection consistency.

---

### 5. Reasoning Agent (LLM SOC Analyst)

Aggregates all signals and produces final classification.

Uses GPT-4.1-mini to analyze:
- IOC signals
- Threat intelligence
- VirusTotal results
- Memory matches

Outputs:
- Final verdict (legit / suspicious / phishing)
- Risk score (0–100)
- Extracted indicators (IOCs)
- SOC-style reasoning explanation

Purpose:
Replaces rule-based classification with LLM reasoning.

---

### 6. Reporting Layer

Generates final SOC-style output.

Outputs:
- Verdict
- Risk score
- Indicators
- SOC explanation

---

## Tool-Based Architecture

Capabilities:
- URL reputation checking
- VirusTotal API integration
- Modular tool system

Future:
- AbuseIPDB
- URLScan.io
- OpenCTI

---

## Memory System

- Stores phishing patterns
- Detects repeated attacks
- Improves contextual reasoning

---

## Risk Scoring

- 0–30 → Legitimate
- 31–60 → Suspicious
- 61–100 → Phishing

---

## Architecture Flow

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
Reporting Layer
    ↓
Final Output
```
---
### LangGraph Workflow

```python
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
```
---
### Tech Stack
- Python
- FastAPI
- LangGraph
- OpenAI GPT-4.1-mini
- VirusTotal API
- React
- TailwindCSS
---
### How to Run
- Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
- Frontend
cd frontend
npm install
npm run dev
---
### Evaluation

Dataset: ~40 emails (phishing, suspicious, legitimate)

Metrics computed using evaluate.py:

- Accuracy
- Precision (macro average)
- Recall (macro average)
- F1 Score (macro average)
- Confusion matrix

### Run Evaluation

```bash
python evaluate.py
```
---
### Measured Results
- Accuracy: ~0.825
- Precision: computed via evaluation script
- Recall: computed via evaluation script
- F1 Score: computed via evaluation script
---
### Dataset

Location:

backend/soc_dataset.py

Includes:

- Phishing emails
- Legitimate emails
- Edge-case phishing (HR scams, Google Forms, spoofing)
---
### Why This Is Agentic

This system is agentic because:

- Multiple specialized agents
- LangGraph orchestration
- Structured state passing
- External tool integration
- LLM-based reasoning agent
- Explainable SOC outputs
---
