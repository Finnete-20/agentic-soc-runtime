import json
from runtime_graph import app as agent_app


# -------------------------
# TEST DATASET (START SMALL)
# -------------------------

TEST_CASES = [
    {
        "label": "phishing",
        "email": """
Urgent: Your Microsoft account has been locked.
Please verify your identity immediately:
http://security-login-microsoft-reset.com
"""
    },
    {
        "label": "legit",
        "email": """
Hi,
Your GitHub weekly digest is ready.
You can view your repository updates in your dashboard.
"""
    },
    {
        "label": "phishing",
        "email": """
Your bank account is suspended.
Login here to restore access:
http://fake-bank-security-check.com
"""
    },
    {
        "label": "legit",
        "email": """
Hello,
Your university tuition receipt has been processed successfully.
No action is required.
"""
    },
    {
        "label": "edge",
        "email": """
Security notice:
We detected unusual activity. If this was you, ignore this message.
"""
    }
]


# -------------------------
# EVALUATION RUNNER
# -------------------------

def run_eval():
    results = []

    correct = 0

    for test in TEST_CASES:
        state = {
            "email_content": test["email"],
            "extracted_iocs": [],
            "threat_data": {},
            "risk_score": 0,
            "investigation_steps": [],
            "final_report": {}
        }

        output = agent_app.invoke(state)
        verdict = output["final_report"]["verdict"]

        is_correct = verdict == test["label"]

        if is_correct:
            correct += 1

        results.append({
            "input_label": test["label"],
            "predicted": verdict,
            "risk_score": output["final_report"]["risk_score"],
            "correct": is_correct
        })

    accuracy = correct / len(TEST_CASES)

    summary = {
        "accuracy": accuracy,
        "total": len(TEST_CASES),
        "correct": correct,
        "results": results
    }

    with open("evaluation_results.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("\nEVALUATION COMPLETE")
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print("Saved to evaluation_results.json")


if __name__ == "__main__":
    run_eval()