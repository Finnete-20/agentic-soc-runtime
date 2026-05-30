import re
from state import AgentState

URL_REGEX = r'https?://[^\s]+'


def extract_iocs(state: AgentState):

    email = state["email_content"]

    signals = []

    urls = re.findall(URL_REGEX, email)

    # -----------------------------
    # STRUCTURAL SIGNAL ENGINE
    # -----------------------------

    signals.append(("length", len(email)))

    signals.append(("word_count", len(email.split())))

    signals.append(("uppercase_ratio",
                     sum(1 for c in email if c.isupper()) / max(len(email), 1)))

    signals.append(("url_count", len(urls)))

    signals.append(("exclamation_count", email.count("!")))

    signals.append(("suspicious_density",
                     sum(1 for w in ["urgent", "verify", "account", "login"]
                         if w in email.lower())))

    state["extracted_iocs"] = signals

    return state