from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from runtime_graph import app as agent_app

app = FastAPI(title="Agentic SOC Phishing Detection System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# INPUT SCHEMA (FIXED)
# -------------------------
class EmailInput(BaseModel):
    email: str


# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/")
def health():
    return {"status": "ok"}


# -------------------------
# MAIN ENDPOINT
# -------------------------
@app.post("/investigate")
def investigate(payload: EmailInput):

    try:
        result = agent_app.invoke({
            "email": payload.email
        })

        return {
            "verdict": result.get("verdict"),
            "risk_score": result.get("risk_score"),
            "reasoning": result.get("reasoning"),
            "iocs": result.get("iocs")
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "verdict": "error",
            "risk_score": 0,
            "reasoning": {}
        }