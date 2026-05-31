import { useState } from "react";
import { analyzeEmail } from "./api";

export default function App() {
  const [email, setEmail] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    try {
      setLoading(true);
      setResult(null);

      const res = await analyzeEmail(email);
      setResult(res);

    } catch (err) {
      setResult({
        verdict: "error",
        risk_score: 0,
        iocs: {}
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>🛡️ Agentic SOC Phishing Detection</h2>

      <textarea
        rows={6}
        style={{ width: "100%" }}
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <button onClick={handleAnalyze}>
        {loading ? "Analyzing..." : "Analyze Email"}
      </button>

      {result?.verdict && (
        <div style={{ marginTop: 20 }}>
          <h3>Verdict: {result.verdict}</h3>
          <p>Risk Score: {result.risk_score}</p>
          <pre>{JSON.stringify(result.iocs, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}