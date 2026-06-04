# AI Phishing Detection System — Evaluation Report

---

## 1. Overview

This evaluation measures the performance of an Agentic SOC Phishing Detection System built using a multi-agent architecture (LangGraph), LLM-assisted reasoning, tool-based intelligence, and memory-augmented decision-making.

The objective is to assess how well the system simulates SOC analyst reasoning compared to a baseline heuristic classifier.

---

## 2. Evaluation Objectives

The evaluation focuses on:

- Effectiveness of multi-agent reasoning pipeline
- Comparison against baseline keyword classifier
- Contribution of memory and threat intelligence signals
- Robustness on edge-case emails
- Consistency of SOC-style risk scoring

---

## 3. Dataset Description

The evaluation dataset contains **20–40 samples (current experimental set)** including:

| Category     | Description                  | Samples |
|--------------|------------------------------|---------|
| Phishing     | Malicious email samples      | ~40%    |
| Legitimate   | Safe email samples           | ~40%    |
| Edge Cases   | Ambiguous security emails    | ~20%    |

## Dataset location:

backend/evaluation/data/

---

## 4. Evaluation Methodology

Each sample is processed using two systems:

---

### 4.1 Agentic SOC System

#### System Pipeline

```text
Email Input
    ↓
IOC Extraction
    ↓
Threat Intelligence
    ↓
Memory Lookup
    ↓
LLM-Based Reasoning Agent
    ↓
LLM-Assisted Reporting Agent
    ↓
Final Classification Output