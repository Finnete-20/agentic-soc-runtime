import re
from state import AgentState
from model_router import route_model

URL_REGEX = r'https?://[^\s]+'

# High-signal phishing keywords (NOT treated as IOCs anymore, only features)
PHISHING_SIGNALS = [
    "urgent",
    "verify",
    "login",
    "password",
    "account",
    "suspended",
    "click",
    "immediately"
]

def extract_iocs(state: AgentState):
    email = state["email_content"].lower()

    model = route_model("ioc_extraction")

    urls = re.findall(URL_REGEX, email)

    # ONLY real IOCs = URLs
    iocs = urls

    # store separately as signals (important improvement)
    state["phishing_signals"] = [
        w for w in PHISHING_SIGNALS if w in email
    ]

    state["extracted_iocs"] = iocs

    state["investigation_steps"].append(
        f"IOC Agent used {model} → extracted {len(urls)} URLs + {len(state['phishing_signals'])} signals"
    )

    return state