import re

def extract_iocs(email: str):

    urls = re.findall(r"http[s]?://\S+", email)

    suspicious_words = sum([
        "urgent" in email.lower(),
        "verify" in email.lower(),
        "password" in email.lower(),
        "login" in email.lower(),
        "account" in email.lower()
    ])

    return {
        "url_count": len(urls),
        "urls": urls,
        "suspicious_words": suspicious_words,
        "uppercase_ratio": sum(c.isupper() for c in email) / max(len(email), 1)
    }