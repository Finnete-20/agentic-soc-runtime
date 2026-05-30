import json
from runtime_graph import app as agent_app

# -----------------------------
# Load dataset
# -----------------------------
def load_data():
    with open("evaluation/data/phishing_samples.json") as f:
        phishing = json.load(f)

    with open("evaluation/data/legit_samples.json") as f:
        legit = json.load(f)

    return phishing + legit


# -----------------------------
# Run full agent system
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

    result = agent_app.invoke(state)
    return result


# -----------------------------
# Simple baseline (NO AGENTS)
# -----------------------------
def run_baseline(email):
    # naive heuristic baseline
    keywords = ["urgent", "verify", "login", "password", "http"]

    score = sum(1 for k in keywords if k in email.lower())

    if score >= 2:
        return "phishing"
    return "legit"


# -----------------------------
# Evaluation loop
# -----------------------------
def evaluate():
    data = load_data()

    full_correct = 0
    base_correct = 0

    for item in data:
        email = item["email"]
        label = item["label"]

        # FULL SYSTEM
        result = run_full_system(email)
        predicted_full = result["final_report"].get("verdict", "legit")

        # BASELINE
        predicted_base = run_baseline(email)

        if predicted_full == label:
            full_correct += 1

        if predicted_base == label:
            base_correct += 1

    total = len(data)

    print("\n=== RESULTS ===")
    print("Full Agentic Accuracy:", round(full_correct / total * 100, 2))
    print("Baseline Accuracy:", round(base_correct / total * 100, 2))


if __name__ == "__main__":
    evaluate()