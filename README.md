# Agentic SOC Phishing Detection System

## Overview
This project is an **agentic AI system for SOC (Security Operations Center) phishing detection**.  
It uses a multi-agent architecture, tool abstraction (MCP-style design), and evaluation-driven development to analyze email content and classify phishing attempts.

---

## Key Features

- Multi-agent workflow using LangGraph
- IOC extraction agent (regex-based)
- Threat intelligence tool layer (MCP-style abstraction)
- Risk reasoning engine with SOC heuristics
- Structured JSON output
- Model routing simulation (task-based intelligence separation)
- Evaluation framework with held-out dataset

---

## Architecture

Email Input  
→ IOC Extraction Agent  
→ Threat Intelligence Tool Layer  
→ Reasoning Agent (Risk Scoring)  
→ Reporting Agent (Final SOC Decision)

---

## Tooling (MCP-style Design)

- `url_reputation_check` tool simulates external security API
- Tool registry pattern enables modular expansion
- Designed for future integration with VirusTotal or real SOC APIs

---

## Evaluation

The system was evaluated using a held-out dataset of:

- Phishing emails
- Legitimate emails
- Edge-case ambiguous emails

### Results:
- Accuracy: ~80%
- Output: structured JSON classification reports

---

## How to Run

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:api --reload
