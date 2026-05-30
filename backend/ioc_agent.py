import re
from state import AgentState
from model_router import route_model

URL_REGEX = r'https?://[^\s]+'


def extract_iocs(state: AgentState):
    email = state["email_content"]

    model = route_model("ioc_extraction")

    # Extract ONLY real URLs
    urls = re.findall(URL_REGEX, email)

    # Extract domains (important upgrade)
    domains = []
    for url in urls:
        try:
            domain = url.split("//")[1].split("/")[0]
            domains.append(domain)
        except:
            pass

    state["extracted_iocs"] = {
        "urls": urls,
        "domains": domains
    }

    state["investigation_steps"].append(
        f"IOC Agent extracted {len(urls)} URLs and {len(domains)} domains using {model}"
    )

    return state