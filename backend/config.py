import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VT_API_KEY = os.getenv("VT_API_KEY")

# ✅ ADD THIS
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.2))