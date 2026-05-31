const BASE_URL = "https://agentic-soc-runtime.onrender.com";

export async function analyzeEmail(email_content) {
  const res = await fetch(`${BASE_URL}/investigate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email_content }),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data?.message || "Backend error");
  }

  return data;
}