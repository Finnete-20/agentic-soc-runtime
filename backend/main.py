from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from runtime_graph import app as agent_app

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/investigate")
def investigate(payload: dict):
    email = payload["email_content"]

    result = agent_app.invoke({"email": email})

    return result["report"]