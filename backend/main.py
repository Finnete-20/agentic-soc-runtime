from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from runtime_graph import app as agent_graph

app = FastAPI(title="SOC Agentic System")

# CORS FIX (frontend connection issue)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "*"
    ],
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

    result = agent_graph.invoke({
        "email": payload.email_content
    })

    # NORMALIZED OUTPUT (VERY IMPORTANT)
    return {
        "verdict": result.get("verdict", "unknown"),
        "risk_score": result.get("risk_score", 0),
        "iocs": result.get("iocs", {}),
        "reasoning": result.get("reasoning", {})
    }