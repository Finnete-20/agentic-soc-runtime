from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/investigate")
def investigate(data: EmailInput):
    return {
        "verdict": "suspicious",
        "risk_score": 37,
        "iocs": ["url_count", "suspicious_words"],
        "threat_data": {}
    }