import os
import time
import requests

VT_API_KEY = os.getenv("VT_API_KEY")


def virustotal_tool(url):
    """
    REAL VirusTotal integration:
    1. Submit URL
    2. Poll for analysis result
    3. Return verdict summary
    """

    if not VT_API_KEY:
        return {"url": url, "error": "Missing VT_API_KEY"}

    headers = {"x-apikey": VT_API_KEY}

    try:
        # STEP 1: submit URL
        submit = requests.post(
            "https://www.virustotal.com/api/v3/urls",
            headers=headers,
            data={"url": url}
        )

        if submit.status_code not in [200, 201]:
            return {"url": url, "error": submit.text}

        analysis_id = submit.json()["data"]["id"]

        # STEP 2: poll for results (IMPORTANT)
        analysis_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"

        for _ in range(5):  # retry loop
            time.sleep(2)

            res = requests.get(analysis_url, headers=headers)

            if res.status_code != 200:
                continue

            data = res.json()

            stats = data.get("data", {}).get("attributes", {}).get("stats", {})

            if stats:
                return {
                    "url": url,
                    "malicious": stats.get("malicious", 0),
                    "suspicious": stats.get("suspicious", 0),
                    "harmless": stats.get("harmless", 0),
                    "source": "virustotal_api"
                }

        # fallback if not ready yet
        return {
            "url": url,
            "analysis_id": analysis_id,
            "status": "pending"
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