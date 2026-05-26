import re
from state import AgentState
from model_router import route_model

URL_REGEX = r'https?://[^\s]+'


def extract_iocs(state: AgentState):
    email = state["email_content"]

    model = route_model("ioc_extraction")

    urls = re.findall(URL_REGEX, email)

    state["extracted_iocs"] = urls

    state["investigation_steps"].append(
        f"IOC Agent used {model} and extracted {len(urls)} URLs"
    )

    return state