import time
import base64
import requests
from config import VT_API_KEY


def virustotal_tool(url):

    if not VT_API_KEY:
        return {"url": url, "error": "Missing VT_API_KEY"}

    headers = {"x-apikey": VT_API_KEY}

    try:
        # encode URL (VirusTotal requirement)
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")

        # submit URL
        submit = requests.post(
            f"https://www.virustotal.com/api/v3/urls/{url_id}",
            headers=headers
        )

        if submit.status_code not in [200, 201]:
            return {"url": url, "error": submit.text}

        analysis_id = submit.json().get("data", {}).get("id")

        analysis_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"

        for _ in range(5):
            time.sleep(2)

            res = requests.get(analysis_url, headers=headers)

            if res.status_code != 200:
                continue

            data = res.json()
            stats = data.get("data", {}).get("attributes", {}).get("stats", {})

            if isinstance(stats, dict) and stats:
                return {
                    "url": url,
                    "malicious": stats.get("malicious", 0),
                    "suspicious": stats.get("suspicious", 0),
                    "harmless": stats.get("harmless", 0),
                    "source": "virustotal_api"
                }

        return {
            "url": url,
            "status": "pending",
            "malicious": 0,
            "suspicious": 0,
            "harmless": 0
        }

    except Exception as e:
        return {"url": url, "error": str(e)}


def virustotal_agent(state):

    urls = state.get("iocs", {}).get("urls", [])

    results = [virustotal_tool(url) for url in urls]

    return {
        **state,
        "virustotal": results
    }