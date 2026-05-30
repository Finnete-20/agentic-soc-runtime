# Agentic SOC Phishing Detection System

# Overview

The Agentic SOC Phishing Detection System is an AI-powered Security Operations Center (SOC) assistant designed to detect phishing emails using a multi-agent architecture.

The system simulates SOC workflows using LangGraph, tool-based intelligence, memory reasoning, and structured reporting.

It focuses on explainability and structured reasoning rather than only classification accuracy.

# Key Features

## Multi-Agent SOC Pipeline

- IOC Extraction Agent
- Threat Intelligence Agent
- Memory Lookup Agent
- Risk Reasoning Engine
- SOC Reporting Agent

## Tool-Based Architecture

- URL reputation checking
- Tool abstraction layer
- Extensible SOC tools design

Future integrations:
- VirusTotal
- AbuseIPDB
- URLScan

## Memory System

- Stores past incidents
- Detects recurring threats
- Improves contextual analysis

## Risk Scoring

0–30 = Legitimate  
31–60 = Suspicious  
61–100 = Phishing

# Architecture

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

# LangGraph Workflow

ioc → threat → memory → reasoning → report

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

# Tech Stack

Python, FastAPI, LangGraph, React, TailwindCSS

# Run

Backend:
cd backend
pip install -r requirements.txt
uvicorn main:api --reload

Frontend:
cd frontend
npm install
npm run dev

Evaluation:
cd backend
python evaluate.py

# Purpose

Multi-agent SOC simulation system for phishing detection with explainability and structured reasoning.