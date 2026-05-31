from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from runtime_graph import app as agent_app

api = FastAPI()

# IMPORTANT: CORS FIX (this is why frontend fails on Render)
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
    return {"status": "ok", "message": "SOC backend running"}


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

    return result.get("final_report", {
        "verdict": "unknown",
        "risk_score": 0,
        "message": "No report generated"
    })


# IMPORTANT: THIS MUST EXIST for uvicorn
app = api