import { useState } from "react";
import { analyzeEmail } from "./api";
import "./App.css";

export default function App() {
  const [email, setEmail] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    if (!email.trim()) {
      setError("Please enter an email first");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await analyzeEmail(email);
      setResult(data || {});
    } catch (err) {
      setError("Backend connection failed");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const loadSample = () => {
    setEmail(`Subject: Urgent Account Verification Required
Your Microsoft 365 account has been flagged.
Verify here: http://security-check-login.net`);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 to-indigo-950 text-white p-6">
      <div className="max-w-3xl mx-auto">

        {/* HEADER */}
        <h1 className="text-3xl font-bold mb-2">
          🛡️ SOC Phishing Detection System
        </h1>
        <p className="text-gray-300 mb-6">
          Multi-Agent Email Threat Analyzer
        </p>

        {/* INPUT BOX */}
        <textarea
          className="w-full h-40 p-4 rounded bg-gray-900 border border-gray-700 text-white"
          placeholder="Paste email content here..."
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        {/* BUTTONS */}
        <div className="flex gap-3 mt-4">
          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded"
          >
            {loading ? "Analyzing..." : "Analyze Email"}
          </button>

          <button
            onClick={loadSample}
            className="bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded"
          >
            Load Sample
          </button>
        </div>

        {/* ERROR */}
        {error && (
          <div className="mt-4 p-3 bg-red-700 rounded">
            {error}
          </div>
        )}

        {/* RESULT */}
        {result?.verdict && (
          <div className="mt-6 p-4 bg-gray-900 rounded border border-gray-700">

            <h2 className="text-xl font-bold mb-2">
              Verdict:{" "}
              <span
                className={
                  result.verdict === "malicious"
                    ? "text-red-500"
                    : result.verdict === "suspicious"
                    ? "text-yellow-400"
                    : "text-green-400"
                }
              >
                {result.verdict}
              </span>
            </h2>

            <p className="mb-2">
              Risk Score:{" "}
              <span className="font-bold">{result.risk_score}</span>
            </p>

            <h3 className="mt-3 font-semibold">IOCs</h3>
            <pre className="text-sm bg-black p-3 rounded overflow-x-auto">
              {JSON.stringify(result.iocs, null, 2)}
            </pre>

            {result.reasoning?.reasons && (
              <>
                <h3 className="mt-3 font-semibold">Reasoning</h3>
                <ul className="list-disc ml-5 text-sm text-gray-300">
                  {result.reasoning.reasons.map((r, i) => (
                    <li key={i}>{r}</li>
                  ))}
                </ul>
              </>
            )}

          </div>
        )}

      </div>
    </div>
  );
}