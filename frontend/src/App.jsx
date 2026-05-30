import { useState } from "react";

export default function App() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const analyzeEmail = async () => {
    setLoading(true);
    setResult(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/investigate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email_content: email,
        }),
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      alert("Backend connection failed");
    }

    setLoading(false);
  };

  return (
    <div style={styles.page}>
      <h1 style={styles.title}>SOC Phishing Detection System</h1>

      <textarea
        style={styles.textarea}
        placeholder="Paste email content here..."
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <button style={styles.button} onClick={analyzeEmail}>
        {loading ? "Analyzing..." : "Analyze Email"}
      </button>

      {result && (
        <div style={styles.card}>
          <h2>Result</h2>

          <p>
            <strong>Verdict:</strong> {result.verdict}
          </p>

          <p>
            <strong>Risk Score:</strong> {result.risk_score.toFixed(2)}
          </p>

          <h3>IOC Features</h3>
          <pre style={styles.code}>
            {JSON.stringify(result.iocs, null, 2)}
          </pre>

          <h3>Threat Data</h3>
          <pre style={styles.code}>
            {JSON.stringify(result.threat_data, null, 2)}
          </pre>

          <h3>Investigation Steps</h3>
          <ul>
            {result.investigation_steps.map((step, i) => (
              <li key={i}>{step}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

const styles = {
  page: {
    fontFamily: "Arial",
    padding: 30,
    maxWidth: 900,
    margin: "0 auto",
  },
  title: {
    textAlign: "center",
    marginBottom: 20,
  },
  textarea: {
    width: "100%",
    height: 150,
    padding: 10,
    fontSize: 14,
    marginBottom: 10,
  },
  button: {
    padding: "10px 20px",
    cursor: "pointer",
    background: "black",
    color: "white",
    border: "none",
    marginBottom: 20,
  },
  card: {
    padding: 20,
    border: "1px solid #ddd",
    borderRadius: 10,
  },
  code: {
    background: "#f4f4f4",
    padding: 10,
    overflowX: "auto",
  },
};