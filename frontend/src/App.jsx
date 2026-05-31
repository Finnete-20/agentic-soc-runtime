import { useState } from "react";
import { analyzeEmail } from "./api";

export default function App() {
  const [email, setEmail] = useState("");
  const [result, setResult] = useState(null);

  const handleAnalyze = async () => {
    const res = await analyzeEmail(email);
    setResult(res || {});
  };

  return (
    <div className="min-h-screen bg-blue-800 text-white p-6">
      <h1 className="text-2xl font-bold">
        🛡️ Agentic SOC Phishing Detection System
      </h1>

      <textarea
        className="w-full mt-4 p-2 text-black"
        rows={6}
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <button
        className="bg-green-500 px-4 py-2 mt-3"
        onClick={handleAnalyze}
      >
        Analyze Email
      </button>

      {result?.verdict && (
        <div className="mt-6 bg-black p-4">
          <h2>Verdict: {result.verdict}</h2>
          <p>Risk Score: {result.risk_score}</p>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}