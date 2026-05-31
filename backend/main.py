from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from runtime_graph import app as agent_app

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailInput(BaseModel):
    email_content: str


@api.get("/")
def health():
    return {"status": "ok"}


@api.post("/investigate")
def investigate(email: EmailInput):

    state = {
        "email_content": email.email_content,
        "extracted_iocs": [],
        "threat_data": {},
        "risk_score": 0,
        "investigation_steps": [],
        "final_report": {}
    }

    result = agent_app.invoke(state)

    report = result.get("final_report", {})

    # IMPORTANT: ALWAYS RETURN JSON OBJECT (not string)
    return {
        "verdict": report.get("verdict", "unknown"),
        "risk_score": report.get("risk_score", 0),
        "iocs": report.get("iocs", []),
        "threat_data": report.get("threat_data", {}),
        "investigation_steps": report.get("investigation_steps", [])
    }


app = api