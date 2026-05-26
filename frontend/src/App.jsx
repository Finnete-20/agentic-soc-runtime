import { useState } from "react";
import axios from "axios";

export default function App() {
  const [email, setEmail] = useState("");
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);

  const runInvestigation = async () => {
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/investigate", {
        email_content: email,
      });

      setReport(res.data);
    } catch (err) {
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white p-10">
      <h1 className="text-3xl font-bold mb-6">
        Agentic SOC Investigation System
      </h1>

      <textarea
        className="w-full h-60 p-4 text-black rounded"
        placeholder="Paste suspicious email here..."
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <button
        className="mt-4 bg-blue-600 px-6 py-2 rounded"
        onClick={runInvestigation}
      >
        {loading ? "Investigating..." : "Run Investigation"}
      </button>

      {report && (
        <div className="mt-8 bg-slate-800 p-4 rounded">
          <h2 className="text-xl font-bold mb-2">SOC Report</h2>
          <pre>{JSON.stringify(report, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}