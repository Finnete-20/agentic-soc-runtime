import os
from dotenv import load_dotenv

if os.path.exists(".env"):
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


class EmailInput(BaseModel):
    email_content: str


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/investigate")
def investigate(payload: EmailInput):
    return agent_app.invoke({
        "email": payload.email_content
    })