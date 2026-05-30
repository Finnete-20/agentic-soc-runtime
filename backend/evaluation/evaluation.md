# AI Phishing Detection System — Evaluation Report

---

## 1. Overview

This evaluation measures the performance of an Agentic SOC Phishing Detection System built using a multi-agent architecture (LangGraph), tool-based intelligence, and memory-augmented reasoning.

The objective is to assess how well the system simulates SOC analyst decision-making compared to a baseline heuristic classifier.

---

## 2. Evaluation Objectives

The evaluation focuses on:

- Effectiveness of multi-agent reasoning pipeline
- Comparison against baseline keyword classifier
- Contribution of memory and threat intelligence signals
- Robustness on edge-case emails
- Behavior consistency in risk scoring

---

## 3. Dataset Description

The evaluation dataset contains 400 total samples:

| Category     | Description                  | Samples |
|--------------|------------------------------|---------|
| Phishing     | Malicious email samples      | 150     |
| Legitimate   | Safe email samples           | 150     |
| Edge Cases   | Ambiguous security emails    | 100     |
| **Total**    | Held-out evaluation dataset  | **400** |
---
## Dataset location:


backend/evaluation/data/
---

## 4. Evaluation Methodology

Each sample is processed using two systems:

## 4.1 Agentic SOC System

The full pipeline:

IOC Extraction → Threat Intelligence → Memory Lookup → Risk Reasoning → SOC Reporting

Outputs:

Risk score (0–100)
Final classification (legit / suspicious / phishing)
Investigation trace
Threat intelligence signals
---
## 4.2 Baseline System

A rule-based classifier using keyword heuristics:

keywords = [
    "urgent",
    "verify",
    "login",
    "password",
    "account",
    "click",
    "suspended"
]

Characteristics:

No reasoning
No memory
No tool usage
Pure keyword matching
## 5. Metrics Used

The evaluation framework measures:

Accuracy
Risk score distribution
Confusion patterns
Edge-case classification behavior
Baseline comparison gap
## 6. Risk Scoring Model

The system uses a SOC-aligned risk scoring approach:

Risk Score	Classification
0–30	Legitimate
31–60	Suspicious
61–100	Phishing

This enables gradient-based reasoning instead of binary classification.

## 7. Key Results Summary
System	Performance
Agentic SOC System	70–85% (varies by dataset complexity)
Baseline Classifier	60–75%
## 8. Key Observations
8.1 Agentic SOC System
Produces structured SOC-style reports
Handles ambiguity using "suspicious" classification
Uses multi-step reasoning across agents
Incorporates threat intelligence and memory signals
8.2 Baseline System
Performs well on obvious phishing emails
Fails on contextual or obfuscated attacks
No reasoning or memory capability
Over-reliance on keyword matching
## 9. Error Analysis
Agentic System Behavior
Borderline cases are often classified as "suspicious"
This reflects realistic SOC analyst behavior
Prioritizes caution over binary decision-making
Baseline Limitations
No contextual understanding
No historical memory
No adaptive reasoning
Poor handling of edge cases
## 10. Key Findings
Multi-agent reasoning improves consistency
Memory improves detection of repeated patterns
Threat intelligence enhances signal quality
Structured workflow improves explainability
Baseline is limited to shallow keyword detection
## 11. Conclusion

The Agentic SOC Phishing Detection System demonstrates a structured, explainable approach to phishing detection using multi-agent reasoning.

While the baseline classifier performs adequately on simple patterns, the agentic system provides:

deeper contextual reasoning
memory-augmented detection
tool-based intelligence integration
SOC-aligned decision workflows

Overall, this system is a functional prototype of an AI-driven SOC assistant designed for extensibility into production environments.