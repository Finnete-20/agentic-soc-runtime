from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VT_API_KEY = os.getenv("VT_API_KEY")

LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.2))