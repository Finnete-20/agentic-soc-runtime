from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from runtime_graph import app as workflow_app

app = FastAPI(title="Agentic SOC System")

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
def investigate(payload: EmailInput):
    result = workflow_app.invoke({
        "email": payload.email_content
    })

    return {
        "verdict": result.get("verdict"),
        "risk_score": result.get("risk_score"),
        "iocs": result.get("iocs", {}),
        "memory": result.get("memory", {}),
        "reasoning": result.get("reasoning", {}),
        "threat": result.get("threat", {})
    }