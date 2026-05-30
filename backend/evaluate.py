import json
from runtime_graph import app as agent_app

# -----------------------
# Load test dataset
# -----------------------
def load_samples():
    with open("evaluation/phishing_samples.json", "r") as f:
        phishing = json.load(f)

    with open("evaluation/legit_samples.json", "r") as f:
        legit = json.load(f)

    return phishing + legit


# -----------------------
# Run model
# -----------------------
def run_agent(email):
    state = {
        "email_content": email,
        "extracted_iocs": [],
        "threat_data": {},
        "risk_score": 0,
        "investigation_steps": [],
        "final_report": {}
    }

    result = agent_app.invoke(state)
    return result


# -----------------------
# Evaluate system
# -----------------------
def evaluate():
    samples = load_samples()

    correct = 0
    total = len(samples)

    for sample in samples:
        result = run_agent(sample["email"])

        predicted = result["final_report"].get("verdict")
        actual = sample["label"]

        if predicted == actual:
            correct += 1

    accuracy = correct / total

    print("\n=== EVALUATION RESULTS ===")
    print("Accuracy:", round(accuracy * 100, 2))


if __name__ == "__main__":
    evaluate()
