import re

def extract_iocs(email: str):
    urls = re.findall(r"http[s]?://\S+", email)

    suspicious_words = any(word in email.lower() for word in [
        "urgent", "verify", "password", "login", "click", "account"
    ])

    return {
        "url_count": len(urls),
        "urls": urls,
        "suspicious_words": 1 if suspicious_words else 0,
        "uppercase_ratio": sum(1 for c in email if c.isupper()) / max(len(email), 1)
    }