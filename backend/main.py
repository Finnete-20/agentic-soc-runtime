import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from runtime_graph import app as agent_app

# ----------------------------
# FastAPI app
# ----------------------------
app = FastAPI(
    title="Agentic SOC Phishing Detection System"
)

# ----------------------------
# CORS CONFIG (FIXED)
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://agentic-soc-runtime-1.onrender.com",
        "https://agentic-soc-runtime.onrender.com",
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Request schema
# ----------------------------
class EmailInput(BaseModel):
    email_content: str

# ----------------------------
# Health check
# ----------------------------
@app.get("/")
def health():
    return {"status": "ok"}

# ----------------------------
# SOC Investigation endpoint
# ----------------------------
@app.post("/investigate")
def investigate(payload: EmailInput):
    try:
        result = agent_app.invoke({
            "email": payload.email_content
        })
        return result
    except Exception as e:
        # Prevent frontend crash if backend fails
        return {
            "verdict": "error",
            "risk_score": 0,
            "reasoning": {
                "signals": [],
                "soc_report": [f"Backend error: {str(e)}"]
            }
        }