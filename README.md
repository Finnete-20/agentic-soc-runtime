# Agentic SOC Phishing Detection System

## Overview

The Agentic SOC Phishing Detection System is an AI-powered Security Operations Center (SOC) assistant designed to detect phishing emails using a multi-agent architecture.

The system simulates SOC-style investigation workflows using LangGraph, tool-based intelligence, memory reasoning, and structured reporting.

The goal is explainability and structured decision-making rather than only classification accuracy.

---

## Key Features

### Multi-Agent SOC Pipeline

The system uses specialized agents:

- IOC Extraction Agent
- Threat Intelligence Agent
- Memory Lookup Agent
- Risk Reasoning Engine
- SOC Reporting Agent

Each agent performs a specific step in the investigation pipeline.

---

### Tool-Based Architecture

A modular tool layer is used for threat intelligence simulation.

Capabilities:

- URL reputation checking
- Tool abstraction layer
- Extensible SOC tool design

Future integrations:

- VirusTotal API
- AbuseIPDB
- URLScan
- OpenCTI

---

### Memory System

The system maintains historical context:

- Stores past incidents
- Detects repeated malicious patterns
- Improves contextual reasoning
- Enhances risk scoring

---

### Risk Scoring

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
IOC Extraction Agent
    ↓
Threat Intelligence Layer
    ↓
Memory Lookup Agent
    ↓
Risk Reasoning Engine
    ↓
SOC Reporting Agent
    ↓
Final Classification Output
```

---

## LangGraph Workflow

Workflow:

ioc → threat → memory → reasoning → report

Implementation:

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
## Tech Stack

Python

FastAPI

LangGraph

React

TailwindCSS

## How to Run

Backend:

cd backend
pip install -r requirements.txt
uvicorn main:api --reload

Frontend:

cd frontend
npm install
npm run dev

## Evaluation:

cd backend
python evaluate.py

## Purpose

This system demonstrates:

Multi-agent reasoning
SOC-style workflows
Tool-based intelligence
Memory-enhanced detection
Explainable phishing detection