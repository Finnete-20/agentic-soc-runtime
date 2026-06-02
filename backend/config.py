import os

# Force deterministic behavior for grading
DETERMINISTIC_MODE = True

# Lock temperature for all LLM calls
LLM_TEMPERATURE = 0 if DETERMINISTIC_MODE else 0.2