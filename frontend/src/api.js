const BASE_URL =
  import.meta.env.MODE === "development"
    ? "http://127.0.0.1:10000"
    : "https://agentic-soc-runtime.onrender.com";

export async function analyzeEmail(email_content) {
  try {
    const res = await fetch(`${BASE_URL}/investigate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email_content }),
    });

    return await res.json();
  } catch (err) {
    return {
      verdict: "error",
      risk_score: 0,
      iocs: {},
      reasoning: {},
    };
  }
}