import { useState } from "react";
import { analyzeEmail } from "./api";

const samples = [
  "Your Microsoft account has been suspended. Click here immediately: http://fake-login.com",
  "URGENT: Payroll update required. Login to verify salary changes.",
  "Security Alert: Unknown login attempt detected from Russia.",
  "You won $1,000,000. Claim your prize within 24 hours!",
  "Password expiring today. Reset here: http://microsoft-reset-secure.net/login"
];

export default function App() {
  const [email, setEmail] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    setResult(null);

    try {
      const data = await analyzeEmail(email);
      setResult(data);
    } catch (err) {
      setResult({ error: "Backend connection failed" });
    }

    setLoading(false);
  };

  const loadSample = () => {
    const random = samples[Math.floor(Math.random() * samples.length)];
    setEmail(random);
  };

  return (
    <div className="container">
      <h1>SOC Phishing Detection System</h1>

      <textarea
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Paste email content here..."
      />

      <div>
        <button onClick={loadSample}>Load Sample Email</button>
        <button onClick={handleAnalyze}>
          {loading ? "Analyzing..." : "Analyze Email"}
        </button>
      </div>

      {result && (
        <pre>{JSON.stringify(result, null, 2)}</pre>
      )}
    </div>
  );
}