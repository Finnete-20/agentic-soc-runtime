import re

def extract_iocs(state):
    text = state["email"]

    urls = re.findall(r"https?://\S+", text)
    emails = re.findall(r"\S+@\S+", text)

    return {
        **state,
        "iocs": {
            "urls": urls,
            "emails": emails,
            "url_count": len(urls)
        }
    }