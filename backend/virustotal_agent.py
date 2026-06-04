def virustotal_tool(url):
    """
    Mock VirusTotal tool (agent tool simulation)
    """

    if not url:
        return None

    # simple heuristic simulation
    if "forms.gle" in url or "google" in url:
        return {
            "url": url,
            "malicious": 2,
            "suspicious": 1,
            "harmless": 50
        }

    return {
        "url": url,
        "malicious": 0,
        "suspicious": 0,
        "harmless": 80
    }


def virustotal_agent(state):

    urls = state.get("iocs", {}).get("urls", [])

    results = []

    for url in urls:
        results.append(virustotal_tool(url))

    return {
        **state,
        "virustotal": results
    }