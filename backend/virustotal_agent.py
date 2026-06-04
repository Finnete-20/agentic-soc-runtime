import os
import time
import requests

VT_API_KEY = os.getenv("VT_API_KEY")


def virustotal_tool(url):

    if not VT_API_KEY:
        return {"url": url, "error": "Missing VT_API_KEY"}

    headers = {"x-apikey": VT_API_KEY}

    try:
        submit = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data={"url": url}
        )

        if submit.status_code not in [200, 201]:
            return {"url": url, "error": submit.text}

        analysis_id = submit.json()["data"]["id"]

        analysis_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"

        for _ in range(5):
            time.sleep(2)

            res = requests.get(analysis_url, headers=headers)

            if res.status_code != 200:
                continue

            stats = res.json().get("data", {}).get("attributes", {}).get("stats", {})

            if stats:
                return {
                    "url": url,
                    "malicious": stats.get("malicious", 0),
                    "suspicious": stats.get("suspicious", 0),
                    "harmless": stats.get("harmless", 0),
                    "source": "virustotal_api"
                }

        return {"url": url, "status": "pending"}

    except Exception as e:
        return {"url": url, "error": str(e)}


def virustotal_agent(state):

    urls = state.get("iocs", {}).get("urls", [])

    results = [virustotal_tool(url) for url in urls]

    return {
        **state,
        "virustotal": results
    }