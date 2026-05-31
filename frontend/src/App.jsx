import { useState } from "react";
import { analyzeEmail } from "./api";

export default function App() {
  const [email, setEmail] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async () => {
    if (!email.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await analyzeEmail(email);
      setResult(res);
    } catch (err) {
      setError("Backend connection failed");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-blue-900 text-white p-6">
      
      {/* HEADER */}
      <h1 className="text-3xl font-bold mb-2">
        🛡️ Agentic SOC Phishing Detection System
      </h1>

      <p className="text-gray-300 mb-4">
        Multi-Agent Email Threat Analyzer
      </p>

      {/* INPUT */}
      <textarea
        className="w-full h-60 p-3 text-black rounded"
        placeholder="Paste email content here..."
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      {/* BUTTON */}
      <button
        onClick={handleAnalyze}
        className="mt-4 px-5 py-2 bg-green-600 rounded hover:bg-green-700"
      >
        {loading ? "Analyzing..." : "Analyze Email"}
      </button>

      {/* ERROR */}
      {error && (
        <div className="mt-4 text-red-400">
          {error}
        </div>
      )}

      {/* RESULTS */}
      {result && (
        <div className="mt-6 bg-gray-900 p-4 rounded">

          <h2 className="text-xl font-bold mb-2">
            Verdict: {result.verdict || "unknown"}
          </h2>

          <p className="mb-2">
            Risk Score: {result.risk_score ?? 0}
          </p>

          {/* SIGNALS */}
          <div className="mb-3">
            <h3 className="font-bold">Signals</h3>
            <ul className="list-disc ml-5">
              {(result.signals || []).length > 0 ? (
                result.signals.map((s, i) => <li key={i}>{s}</li>)
              ) : (
                <li>No signals detected</li>
              )}
            </ul>
          </div>

          {/* SOC REPORT */}
          <div className="mb-3">
            <h3 className="font-bold">SOC Report</h3>
            <ul className="list-disc ml-5">
              {(result.soc_report || []).length > 0 ? (
                result.soc_report.map((r, i) => <li key={i}>{r}</li>)
              ) : (
                <li>No SOC reasoning available</li>
              )}
            </ul>
          </div>

          {/* RAW DEBUG (optional but useful for grading) */}
          <details className="mt-3">
            <summary className="cursor-pointer text-gray-400">
              Raw Output
            </summary>
            <pre className="text-xs bg-black p-2 mt-2 overflow-auto">
              {JSON.stringify(result, null, 2)}
            </pre>
          </details>

        </div>
      )}
    </div>
  );
}