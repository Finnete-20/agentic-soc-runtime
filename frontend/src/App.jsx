import { useState } from "react";
import { analyzeEmail } from "./api";

export default function App() {
  const [email, setEmail] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const loadSample = () => {
    setEmail(`Subject: Urgent Account Verification Required

Your Microsoft 365 account has been flagged.

Verify here:
http://security-check-login.net

Failure to act within 2 hours will result in suspension.`);
  };

  const handleAnalyze = async () => {
    if (!email.trim()) return;

    setLoading(true);

    try {
      const data = await analyzeEmail(email);
      setResult(data);
    } catch (err) {
      console.error(err);

      setResult({
        verdict: "error",
        risk_score: 0,
        signals: [],
        soc_report: ["Backend connection failed"],
      });
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-blue-900 text-white p-8">
      <div className="max-w-5xl mx-auto">

        <h1 className="text-4xl font-bold mb-2">
          🛡️ Agentic SOC Phishing Detection System
        </h1>

        <p className="text-blue-200 mb-6">
          Multi-Agent Email Threat Analyzer
        </p>

        <textarea
          className="w-full h-72 p-4 rounded text-black"
          placeholder="Paste suspicious email here..."
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <div className="mt-4 flex gap-3">
          <button
            onClick={loadSample}
            className="bg-gray-600 px-4 py-2 rounded"
          >
            Load Sample Email
          </button>

          <button
            onClick={handleAnalyze}
            className="bg-green-600 px-4 py-2 rounded"
            disabled={loading}
          >
            {loading ? "Analyzing..." : "Analyze Email"}
          </button>
        </div>

        {result && (
          <div className="mt-8 bg-slate-800 rounded p-6">

            <h2 className="text-2xl font-bold mb-3">
              Verdict: {result.verdict}
            </h2>

            <p className="text-lg mb-6">
              Risk Score: {result.risk_score}
            </p>

            {/* Signals */}
            <h3 className="text-xl font-semibold mb-2">
              Signals
            </h3>

            {result.reasoning?.signals?.length > 0 ? (
              <ul className="list-disc pl-6 mb-6">
                {result.reasoning.signals.map((signal, index) => (
                  <li key={index}>{signal}</li>
                ))}
              </ul>
            ) : (
              <p className="mb-6">No signals detected</p>
            )}

            {/* SOC REPORT */}
            <h3 className="text-xl font-semibold mb-2">
              SOC Report
            </h3>

            {result.reasoning?.soc_report?.length > 0 ? (
              <ul className="list-disc pl-6 mb-6">
                {result.reasoning.soc_report.map((item, index) => (
                  <li key={index}>{item}</li>
                ))}
              </ul>
            ) : (
              <p className="mb-6">
                No SOC reasoning available
              </p>
            )}

            {/* RAW OUTPUT */}
            <h3 className="text-xl font-semibold mb-2">
              Raw Output
            </h3>

            <pre className="bg-black p-4 rounded overflow-auto text-sm">
              {JSON.stringify(result, null, 2)}
            </pre>

          </div>
        )}

      </div>
    </div>
  );
}