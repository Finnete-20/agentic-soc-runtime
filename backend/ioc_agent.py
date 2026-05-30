import re
from state import AgentState

URL_REGEX = r'https?://[^\s]+'

SUSPICIOUS_KEYWORDS = [
    "urgent",
    "verify",
    "password",
    "login",
    "account",
    "immediately",
    "suspended",
    "click"
]


def extract_iocs(state: AgentState):
    email = state["email_content"].lower()

    urls = re.findall(URL_REGEX, email)

    keywords_found = [
        kw for kw in SUSPICIOUS_KEYWORDS if kw in email
    ]

    # combine both into "IOCs"
    iocs = urls + keywords_found

    state["extracted_iocs"] = iocs

    state["investigation_steps"].append(
        f"IOC Agent extracted {len(iocs)} indicators (urls + keywords)"
    )

    return state