from dotenv import load_dotenv
import os

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY missing in .env")

from runtime_graph import app as agent_app
from soc_dataset import SOC_DATASET


# -----------------------------
# SOC-STYLE LABEL MAPPING
# -----------------------------

def normalize_label(label):
    """
    Dataset label conversion:
    0 = legit
    1 = suspicious
    2 = phishing
    """

    if label == 0 or label == "legit":
        return 0
    elif label == 1 or label == "suspicious":
        return 1
    elif label == 2 or label == "phishing":
        return 2

    return 0


def normalize_pred(pred):
    """
    Model output normalization
    """

    pred = str(pred).lower()

    if "phishing" in pred:
        return 2
    elif "suspicious" in pred:
        return 1
    else:
        return 0


# -----------------------------
# EVALUATION
# -----------------------------

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
    # CONFUSION MATRIX (3-class)
    # -----------------------------

    labels = [0, 1, 2]  # legit, suspicious, phishing

    matrix = {
        (i, j): 0 for i in labels for j in labels
    }

    for t, p in zip(y_true, y_pred):
        matrix[(t, p)] += 1

    print("\n==============================")
    print("CONFUSION MATRIX")
    print("==============================")

    print("Rows = TRUE | Cols = PREDICTED")
    print("0 = legit | 1 = suspicious | 2 = phishing\n")

    for i in labels:
        row = [matrix[(i, j)] for j in labels]
        print(f"{i}: {row}")

    # -----------------------------
    # ACCURACY
    # -----------------------------

    correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)
    accuracy = correct / len(y_true)

    print("\n==============================")
    print("FINAL RESULTS")
    print("==============================")

    print("Accuracy:", round(accuracy, 3))


# -----------------------------
# RUN
# -----------------------------

if __name__ == "__main__":
    evaluate(SOC_DATASET)