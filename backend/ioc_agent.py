import re

def extract_iocs(state):
    text = state["email"]

    urls = re.findall(r"https?://\S+", text)
    emails = re.findall(r"[\w\.-]+@[\w\.-]+", text)

    suspicious_words = sum([
        "urgent" in text.lower(),
        "verify" in text.lower(),
        "password" in text.lower(),
        "login" in text.lower(),
        "account" in text.lower()
    ])

    domains = [e.split("@")[-1] for e in emails]

    return {
        **state,
        "iocs": {
            "urls": urls,
            "emails": emails,
            "domains": domains,
            "url_count": len(urls),
            "suspicious_words": suspicious_words
        }
    }