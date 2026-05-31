from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailInput(BaseModel):
    email_content: str


def analyze_email(email: str):
    text = email.lower()

    length = len(email)
    word_count = len(email.split())
    url_count = len(re.findall(r"http|https|www", text))
    exclamations = email.count("!")
    uppercase_ratio = sum(1 for c in email if c.isupper()) / max(len(email), 1)

    suspicious_keywords = [
        "urgent", "verify", "password", "account", "suspended",
        "login", "click", "immediately", "confirm"
    ]

    suspicious_hits = sum(1 for w in suspicious_keywords if w in text)

    risk_score = (
        url_count * 25 +
        suspicious_hits * 10 +
        exclamations * 5 +
        (uppercase_ratio * 20)
    )

    if risk_score > 60:
        verdict = "phishing"
    elif risk_score > 30:
        verdict = "suspicious"
    else:
        verdict = "safe"

    return {
        "verdict": verdict,
        "risk_score": round(risk_score, 2),
        "iocs": {
            "length": length,
            "word_count": word_count,
            "url_count": url_count,
            "exclamation_count": exclamations,
            "suspicious_keywords_found": suspicious_hits
        }
    }


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/investigate")
def investigate(data: EmailInput):
    return analyze_email(data.email_content)