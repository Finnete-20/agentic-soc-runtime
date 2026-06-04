from dotenv import load_dotenv
import os

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY missing in .env")

from runtime_graph import app as agent_app
from soc_dataset import SOC_DATASET


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

        pred = result.get("verdict", "legit")

        y_pred.append(1 if pred == "phishing" else 0)
        y_true.append(item["label"])

        print("\n==============================")
        print("EMAIL:\n")
        print(item["email"].strip())
        print("EXPECTED:", item["label"])
        print("PREDICTED:", pred)
        print("==============================")

    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
    tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)

    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    accuracy = (tp + tn) / len(y_true)

    print("\n==============================")
    print("FINAL RESULTS")
    print("==============================")

    print("Accuracy :", round(accuracy, 3))
    print("Precision:", round(precision, 3))
    print("Recall   :", round(recall, 3))

    print("\nConfusion Matrix")
    print("TP:", tp)
    print("FP:", fp)
    print("FN:", fn)
    print("TN:", tn)


if __name__ == "__main__":
    evaluate(SOC_DATASET)