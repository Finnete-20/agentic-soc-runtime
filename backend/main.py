from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from runtime_graph import app as agent_app
from pydantic import BaseModel

app = FastAPI(title="SOC Agentic System")

# FIX CORS (this is why frontend breaks)
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
    result = agent_app.invoke({
        "email": payload.email_content
    })
    return result