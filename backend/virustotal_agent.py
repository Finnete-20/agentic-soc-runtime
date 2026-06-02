def virustotal_lookup(state):

    urls = state.get("iocs", {}).get("urls", [])

    results = []

    for url in urls:
        results.append({
            "url": url,
            "malicious": 2,
            "suspicious": 1,
            "harmless": 50
        })

    return {
        **state,
        "virustotal": results
    }