# AI Phishing Detection System — Evaluation Report

# Objective

Evaluate a multi-agent SOC phishing detection system vs a baseline keyword classifier.

Focus:
- reasoning quality
- SOC alignment
- ambiguity handling
- risk scoring

# Systems

## Agentic SOC System

IOC → Threat → Memory → Reasoning → Reporting

## Baseline System

Keyword rules:
urgent, verify, login, password, account, click, suspended

# Dataset

Phishing: 150  
Legit: 150  
Edge Cases: 100  
Total: 400

# Evaluation Method

Each email is processed by:

1. Agentic SOC pipeline  
2. Baseline classifier  

# Metrics

- Accuracy
- Risk distribution
- Confusion behavior
- Edge-case handling

# Risk Levels

0–30 = Legitimate  
31–60 = Suspicious  
61–100 = Phishing  

# Key Observations

Agentic system:
- Uses multi-step reasoning
- Handles uncertainty
- Produces SOC-style explanations

Baseline:
- Keyword dependent
- No reasoning
- No memory

# Conclusion

The agentic system improves explainability and SOC-aligned reasoning compared to baseline classification.