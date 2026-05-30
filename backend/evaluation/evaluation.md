# AI Phishing Detection System – Evaluation Report

## 1. Purpose of Evaluation

This evaluation measures the performance of an AI-powered phishing detection system built using a **multi-agent architecture (LangGraph)**, FastAPI backend, and MCP-style tool abstraction.

The goal is to assess:

- Effectiveness of multi-agent reasoning (IOC → Threat → Memory → Reasoning → Reporting)
- Improvement over a baseline heuristic classifier
- Robustness of structured SOC-style decision making
- Contribution of memory and threat intelligence signals

The evaluation is conducted on a held-out dataset stored in:

- `backend/evaluation/data/phishing_samples.json`
- `backend/evaluation/data/legit_samples.json`
- `backend/evaluation/data/edge_cases.json`

---

## 2. Evaluation Methodology

Each email is processed through two systems:

### 2.1 Full Agentic System

Pipeline:

```
IOC Extraction → Threat Intelligence → Memory Lookup → Reasoning Engine → SOC Reporting
```

Outputs:

- Risk score (0–100)
- Verdict (phishing / suspicious / legit)
- Investigation steps
- Threat intelligence signals

---

### 2.2 Baseline System

A rule-based classifier using keyword heuristics:

```
urgent
login
verify
account
password
click
suspended
```

No reasoning, memory, or external tools are used.

---

## 3. Dataset Summary

| Category | Description | Samples |
|----------|------------|---------|
| Phishing | Malicious email samples | 150 |
| Legitimate | Safe email samples | 150 |
| Edge Cases | Ambiguous security emails | 100 |
| **Total** | Held-out evaluation set | **400** |

---

## 4. Metrics

The system is evaluated using:

- Accuracy
- Risk distribution
- Confusion analysis
- Edge-case behavior analysis

---

## 5. Overall Performance

| System | Performance |
|--------|------------|
| Agentic SOC System | ~70–85% (varies with dataset complexity) |
| Baseline Keyword Model | ~60–75% |

---

## 6. Key Observations

### 6.1 Full Agentic System

- Produces structured SOC-style reports
- Uses multi-step reasoning across agents
- Detects both explicit and subtle phishing patterns
- Handles ambiguous cases using “suspicious” classification

---

### 6.2 Baseline System

- Performs well on obvious keyword-based phishing
- Fails on contextual or low-signal attacks
- No memory or reasoning capability
- No uncertainty modeling

---

## 7. Error & Behavior Analysis

### 7.1 Agentic System Behavior

The system may classify borderline cases as **“suspicious”** rather than strictly phishing.

This reflects **real SOC analyst decision-making**, not binary classification behavior.

---

### 7.2 Baseline Limitations

- Over-reliance on keyword matching
- No contextual reasoning
- No memory of past incidents
- No adaptability to obfuscated attacks

---

## 8. Risk Scoring Behavior

Observed behavior:

- High-risk phishing emails: 70–100
- Legitimate emails: 0–30
- Ambiguous cases: 30–70

This demonstrates a **gradient-based reasoning model**, not a binary classifier.

---

## 9. System Strengths

- Multi-agent SOC-style architecture
- MCP-style tool abstraction for threat intelligence
- Memory-enhanced detection of repeated patterns
- Structured JSON outputs for reliability
- Explainable decision pipeline for SOC workflows

---

## 10. System Limitations

- Heavily rule-based (not ML-trained)
- Synthetic dataset bias affects evaluation stability
- No live external threat intelligence API
- IOC extraction partially keyword-driven
- Limited memory dataset coverage

---

## 11. Key Findings

- Multi-agent reasoning improves consistency over baseline
- Memory + threat intelligence improve detection quality
- Baseline performs well only on shallow keyword patterns
- Agentic system handles ambiguity more effectively
- Structured SOC pipeline improves explainability

---

## 12. Conclusion

The agentic SOC phishing detection system demonstrates **meaningful improvement in reasoning quality and explainability over a baseline heuristic classifier**.

While the baseline performs competitively on simple keyword-based detection, the full system provides:

- deeper contextual reasoning
- multi-step agent collaboration
- memory-enhanced detection
- structured SOC reporting aligned with analyst workflows

Overall, this system represents a **functional prototype of an AI-driven SOC assistant**, designed for extensibility into production-grade security operations rather than purely optimized accuracy.