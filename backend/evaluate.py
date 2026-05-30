import json
from collections import defaultdict
from runtime_graph import app as agent_app

# -----------------------------
# LOAD DATASET
# -----------------------------
def load_data():
    with open("evaluation/data/phishing_samples.json") as f:
        phishing = json.load(f)

    with open("evaluation/data/legit_samples.json") as f:
        legit = json.load(f)

    with open("evaluation/data/edge_cases.json") as f:
        edge = json.load(f)

    return phishing + legit + edge


# -----------------------------
# RUN SYSTEM
# -----------------------------
def run_full_system(email):
    state = {
        "email_content": email,
        "extracted_iocs": [],
        "threat_data": {},
        "memory_matches": [],
        "risk_score": 0,
        "investigation_steps": [],
        "final_report": {}
    }

    return agent_app.invoke(state)


# -----------------------------
# BASELINE
# -----------------------------
def run_baseline(email):
    keywords = ["urgent", "verify", "login", "password", "account", "click", "suspended"]
    score = sum(1 for k in keywords if k in email.lower())
    return "phishing" if score >= 3 else "legit"


# -----------------------------
# NORMALIZATION (SOC STYLE)
# -----------------------------
def normalize(verdict, risk=None):
    if risk is not None:
        if risk >= 60:
            return "phishing"
        if risk >= 30:
            return "suspicious"
        return "legit"

    return "legit" if verdict == "legit" else "phishing"


# -----------------------------
# MAIN EVALUATION
# -----------------------------
def evaluate():
    data = load_data()

    results = {
        "total": len(data),
        "full_correct": 0,
        "baseline_correct": 0,
        "confusion": defaultdict(int),
        "risk_buckets": {"low": 0, "medium": 0, "high": 0}
    }

    print(f"\nRunning SOC evaluation on {len(data)} samples...\n")

    for i, item in enumerate(data):
        email = item["email"]
        label = item["label"]

        # FULL SYSTEM
        result = run_full_system(email)
        report = result["final_report"]

        predicted = report.get("verdict", "legit")
        risk = report.get("risk_score", 0)

        # BASELINE
        baseline = run_baseline(email)

        # NORMALIZED
        final_pred = normalize(predicted, risk)

        # -----------------------------
        # METRICS
        # -----------------------------
        if final_pred == label:
            results["full_correct"] += 1

        if baseline == label:
            results["baseline_correct"] += 1

        # confusion tracking
        results["confusion"][(label, final_pred)] += 1

        # risk buckets
        if risk >= 60:
            results["risk_buckets"]["high"] += 1
        elif risk >= 30:
            results["risk_buckets"]["medium"] += 1
        else:
            results["risk_buckets"]["low"] += 1

        if i % 200 == 0:
            print(f"Processed {i}/{len(data)} samples...")

    # -----------------------------
    # FINAL SCORES
    # -----------------------------
    total = results["total"]

    full_acc = results["full_correct"] / total * 100
    base_acc = results["baseline_correct"] / total * 100

    # -----------------------------
    # PRINT REPORT
    # -----------------------------
    print("\n=== RESULTS ===")
    print(f"Full Agentic Accuracy: {full_acc:.2f}%")
    print(f"Baseline Accuracy: {base_acc:.2f}%")

    print("\n=== SOC ANALYSIS ===")
    print("Risk Distribution:", dict(results["risk_buckets"]))

    print("\n=== SUMMARY ===")
    print(f"Improvement: {full_acc - base_acc:.2f}%")

    # -----------------------------
    # SAVE REPORT (IMPORTANT)
    # -----------------------------
    with open("evaluation/evaluation_report.json", "w") as f:
        json.dump({
            "accuracy": {
                "agentic": full_acc,
                "baseline": base_acc
            },
            "confusion": {str(k): v for k, v in results["confusion"].items()},
            "risk_distribution": results["risk_buckets"]
        }, f, indent=2)


if __name__ == "__main__":
    evaluate()