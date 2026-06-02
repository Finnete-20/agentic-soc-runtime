import json
from sklearn.metrics import confusion_matrix, roc_curve, auc

from runtime_graph import app as agent_app


def load_data():
    with open("evaluation/data/phishing_samples.json") as f:
        phishing = json.load(f)

    with open("evaluation/data/legit_samples.json") as f:
        legit = json.load(f)

    return phishing + legit


def run_system(email):
    return agent_app.invoke({"email": email})


def run_baseline(email):
    keywords = [
        "urgent", "verify", "login", "password",
        "account", "click", "suspended",
        "phone", "email address"
    ]
    score = sum(1 for k in keywords if k in email.lower())
    return "phishing" if score >= 2 else "legit"


def label_to_num(label):
    return 1 if label == "phishing" else 0


def risk_to_prob(risk):
    return risk / 100.0


def evaluate():

    data = load_data()

    y_true = []
    y_agent = []
    y_base = []

    y_agent_prob = []
    y_base_prob = []

    for i, item in enumerate(data):

        email = item["email"]
        label = item["label"]

        result = run_system(email)
        risk = result.get("risk_score", 0)

        agent_label = "phishing" if risk >= 40 else "legit"
        base_label = run_baseline(email)

        y_true.append(label_to_num(label))
        y_agent.append(label_to_num(agent_label))
        y_base.append(label_to_num(base_label))

        y_agent_prob.append(risk_to_prob(risk))
        y_base_prob.append(0.8 if base_label == "phishing" else 0.2)

        if i % 100 == 0:
            print(f"Processed {i}/{len(data)}")

    # ---------------- CONFUSION MATRIX ----------------
    print("\nAgent Confusion Matrix:")
    print(confusion_matrix(y_true, y_agent))

    print("\nBaseline Confusion Matrix:")
    print(confusion_matrix(y_true, y_base))

    # ---------------- ROC AUC ----------------
    fpr_a, tpr_a, _ = roc_curve(y_true, y_agent_prob)
    fpr_b, tpr_b, _ = roc_curve(y_true, y_base_prob)

    print("\nAgent AUC:", auc(fpr_a, tpr_a))
    print("Baseline AUC:", auc(fpr_b, tpr_b))

    print("\nDONE")


if __name__ == "__main__":
    evaluate()