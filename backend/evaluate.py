from dotenv import load_dotenv
import os

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY missing in .env")

from runtime_graph import app as agent_app
from soc_dataset import SOC_DATASET


# -----------------------------
# DATASET LABELS
# 0 = Legit
# 1 = Phishing
# -----------------------------

def normalize_label(label):
    return 0 if label == 0 else 1


def normalize_pred(pred):
    pred = str(pred).lower().strip()

    # Treat suspicious as phishing for evaluation
    if pred in ["phishing", "suspicious"]:
        return 1

    return 0


def evaluate(dataset):

    y_true = []
    y_pred = []

    print("\n==============================")
    print("TOTAL EMAILS:", len(dataset))
    print("==============================")

    for item in dataset:

        result = agent_app.invoke({
            "email": item["email"]
        })

        pred_label = result.get("verdict", "legit")

        true_val = normalize_label(item["label"])
        pred_val = normalize_pred(pred_label)

        y_true.append(true_val)
        y_pred.append(pred_val)

        print("\n==============================")
        print("EMAIL:\n")
        print(item["email"].strip())
        print("EXPECTED:", item["label"])
        print("PREDICTED:", pred_label)
        print("==============================")

    # -----------------------------
    # CONFUSION MATRIX
    # -----------------------------

    labels = [0, 1]

    matrix = {(i, j): 0 for i in labels for j in labels}

    for t, p in zip(y_true, y_pred):
        matrix[(t, p)] += 1

    print("\n==============================")
    print("CONFUSION MATRIX")
    print("==============================")
    print("0 = Legit | 1 = Phishing\n")

    for i in labels:
        row = [matrix[(i, j)] for j in labels]
        print(f"{i}: {row}")

    # -----------------------------
    # ACCURACY
    # -----------------------------

    correct = sum(
        1 for t, p in zip(y_true, y_pred)
        if t == p
    )

    accuracy = correct / len(y_true)

    # -----------------------------
    # PRECISION / RECALL / F1
    # -----------------------------

    precisions = []
    recalls = []
    f1s = []

    for c in labels:

        tp = matrix[(c, c)]

        fp = sum(
            matrix[(o, c)]
            for o in labels
            if o != c
        )

        fn = sum(
            matrix[(c, o)]
            for o in labels
            if o != c
        )

        precision = tp / (tp + fp) if (tp + fp) else 0
        recall = tp / (tp + fn) if (tp + fn) else 0

        if precision + recall:
            f1 = 2 * precision * recall / (precision + recall)
        else:
            f1 = 0

        precisions.append(precision)
        recalls.append(recall)
        f1s.append(f1)

    print("\n==============================")
    print("FINAL RESULTS")
    print("==============================")

    print(f"Accuracy : {accuracy:.3f}")
    print(f"Precision: {sum(precisions)/2:.3f}")
    print(f"Recall   : {sum(recalls)/2:.3f}")
    print(f"F1 Score : {sum(f1s)/2:.3f}")


if __name__ == "__main__":
    evaluate(SOC_DATASET)