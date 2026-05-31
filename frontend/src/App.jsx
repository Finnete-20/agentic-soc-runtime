import { useState } from "react";
import { analyzeEmail } from "./api";
import "./App.css";

export default function App() {
  const [email, setEmail] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!email) return;

    setLoading(true);
    setResult(null);

    const data = await analyzeEmail(email);
    setResult(data);

    setLoading(false);
  };

  return (
    <div style={{ padding: 20, fontFamily: "sans-serif" }}>
      <h2>SOC Phishing Detection System</h2>

      <textarea
        rows="8"
        style={{ width: "100%" }}
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <button onClick={handleAnalyze} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Email"}
      </button>

      {result && (
        <div style={{ marginTop: 20 }}>
          <h3>Verdict: {result.verdict}</h3>
          <p>Risk Score: {result.risk_score}</p>

          <pre>{JSON.stringify(result.iocs, null, 2)}</pre>

          <pre>{JSON.stringify(result.reasoning, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}