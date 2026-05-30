# Agentic SOC Phishing Detection System

## Overview

This project is an **agentic AI system for Security Operations Center (SOC) phishing detection**.

It uses a **multi-agent architecture built with LangGraph**, combined with a **tool-based abstraction layer (MCP-style design)** to analyze email content and classify phishing attempts with explainable reasoning.

Unlike traditional machine learning classifiers, this system focuses on:

- structured decision-making
- step-by-step SOC-style investigation
- tool-augmented security analysis
- explainable outputs for analysts

---

## Key Features

### Multi-Agent SOC Workflow

The system decomposes phishing detection into specialized agents:

- IOC Extraction Agent (extracts indicators of compromise)
- Threat Intelligence Agent (simulates URL reputation analysis)
- Memory Agent (checks historical incidents)
- Reasoning Agent (computes risk score)
- Reporting Agent (final SOC classification)

---

### Tool-Based Architecture (MCP-Style Design)

The system uses a modular tool abstraction layer inspired by MCP (Model Context Protocol):

- `url_reputation_check` simulates external threat intelligence APIs
- Tool registry pattern allows plug-and-play extensions
- Designed for future integration with real SOC tools (VirusTotal, AbuseIPDB, etc.)

---

### Risk-Based Reasoning Engine

Instead of simple binary classification, the system computes:

- Risk score (0–100)
- SOC classification:
  - 0–30 → Legitimate
  - 30–60 → Suspicious
  - 60–100 → Phishing

This reflects real SOC analyst decision-making.

---

## Architecture

### System Flow

```
┌───────────────┐
│ Email Input   │
└──────┬────────┘
       ↓
┌───────────────┐
│ IOC Extraction │
└──────┬────────┘
       ↓
┌────────────────────────────┐
│ Threat Intelligence Layer  │
└──────┬─────────────────────┘
       ↓
┌────────────────────────────┐
│ Memory Lookup Agent        │
└──────┬─────────────────────┘
       ↓
┌────────────────────────────┐
│ Risk Reasoning Engine      │
└──────┬─────────────────────┘
       ↓
┌────────────────────────────┐
│ SOC Reporting Agent        │
└──────┬─────────────────────┘
       ↓
┌────────────────────────────┐
│ Final Classification       │
└────────────────────────────┘
```


---

### Code Mapping

| Step | Implementation File |
|------|--------------------|
| Email Input | `main.py` |
| IOC Extraction Agent | `ioc_agent.py` |
| Threat Intelligence Layer | `threat_agent.py` |
| Memory Lookup Agent | `memory_agent.py` |
| Risk Reasoning Engine | `reasoning_agent.py` |
| SOC Reporting Agent | `reporting_agent.py` |

---
## LangGraph Workflow

The system is implemented using **LangGraph**, enabling a structured multi-agent pipeline for SOC-style phishing analysis.

### Workflow Execution Order

```
ioc → threat → memory → reasoning → report
```

---

### Graph Definition

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

---

## Evaluation

The system is evaluated using a **held-out dataset** containing:

- Phishing emails  
- Legitimate emails  
- Edge-case ambiguous emails  

---

## Evaluation Method

Each sample is processed through:

- Full agentic SOC pipeline  
- Baseline keyword-based classifier  

---

## Baseline Model

A simple heuristic classifier:

```python
keywords = ["urgent", "verify", "login", "password", "account", "click", "suspended"]
```

---

## Metrics

- Accuracy  
- Risk distribution  
- Confusion analysis  
- Edge-case behavior analysis  

---

## Results

| System | Performance |
|--------|------------|
| Agentic SOC System | ~70–85% (varies with dataset complexity) |
| Baseline Keyword Model | ~60–75% |

---

## Key Insight

The agentic system prioritizes:

- explainability  
- structured reasoning  
- SOC-aligned decision making  

rather than pure keyword-based accuracy.

This makes it more realistic for Security Operations Center workflows.

---

## Strengths

- Multi-agent reasoning pipeline  
- Tool-based threat intelligence abstraction  
- Memory-enhanced detection capability  
- Structured SOC reporting output  
- Extensible architecture for production systems  

---

## Limitations

- Heavily rule-based (not ML-trained)  
- Synthetic dataset bias affects evaluation  
- Limited real-world threat intelligence integration  
- Baseline model may outperform on simple keyword datasets  

---

## How to Run

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:api --reload
```

---

## Future Improvements

- Integration with real threat intelligence APIs (VirusTotal, AbuseIPDB)  
- Embedding-based phishing detection model  
- Confusion matrix + ROC-AUC evaluation  
- SOC dashboard visualization UI  
- Real email ingestion pipeline (IMAP/Gmail API)  

---

## Conclusion

This project demonstrates a **prototype SOC agent system** that applies:

- multi-agent reasoning  
- tool-augmented intelligence  
- structured security workflows  

It is designed as a foundation for **AI-assisted Security Operations Centers**, focusing on explainability, modularity, and real-world SOC behavior rather than purely statistical accuracy.
