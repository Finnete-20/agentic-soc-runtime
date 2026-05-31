import { useState } from "react";

const API_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const SAMPLE_EMAILS = [
  `Subject: Urgent Account Verification Required

Dear User,
Your Microsoft 365 account has been suspended due to suspicious activity.
Click here immediately:
http://security-verification-login.com`,

  `Subject: Password Expiring Today

Your email password expires in 2 hours.
Reset now:
http://microsoft-reset-secure.net/login`,

  `Subject: Payroll Update

HR Notice:
Confirm bank details here:
http://payroll-secure-update.com`
];

export default function App() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const loadSampleEmail = () => {
    const random =
      SAMPLE_EMAILS[Math.floor(Math.random() * SAMPLE_EMAILS.length)];
    setEmail(random);
    setResult(null);
  };

  const analyzeEmail = async () => {
    if (!email.trim()) return alert("Paste or load email first");

    setLoading(true);
    setResult(null);

    try {
      const res = await fetch(`${API_URL}/investigate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email_content: email }),
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

      <div style={styles.row}>
        <button style={styles.secondaryBtn} onClick={loadSampleEmail}>
          Load Sample Email
        </button>

        <button style={styles.primaryBtn} onClick={analyzeEmail}>
          {loading ? "Analyzing..." : "Analyze Email"}
        </button>
      </div>

      {result && (
        <div style={styles.card}>
          <h2 style={styles.sectionTitle}>Result</h2>

          <p><b>Verdict:</b> {result.verdict}</p>

          <p>
            <b>Risk Score:</b>{" "}
            {Number(result.risk_score).toFixed(2)}
          </p>

          <h3 style={styles.sectionTitle}>IOC Features</h3>
          <pre style={styles.pre}>
            {JSON.stringify(result.iocs, null, 2)}
          </pre>

          <h3 style={styles.sectionTitle}>Threat Data</h3>
          <pre style={styles.pre}>
            {JSON.stringify(result.threat_data, null, 2)}
          </pre>

          <h3 style={styles.sectionTitle}>Investigation Steps</h3>
          <ul>
            {result.investigation_steps?.map((step, i) => (
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
    maxWidth: 900,
    margin: "0 auto",
    padding: 30,
    background: "#f5f7fb",
    minHeight: "100vh",
    color: "#111", // 🔥 GLOBAL TEXT FIX
  },

  title: {
    textAlign: "center",
    marginBottom: 20,
  },

  textarea: {
    width: "100%",
    height: 180,
    padding: 12,
    fontSize: 14,
    borderRadius: 8,
    border: "1px solid #ccc",
    background: "#fff",
    color: "#111",
  },

  row: {
    display: "flex",
    gap: 10,
    marginTop: 10,
    marginBottom: 20,
  },

  primaryBtn: {
    padding: "10px 18px",
    background: "#000",
    color: "#fff",
    border: "none",
    borderRadius: 6,
    cursor: "pointer",
  },

  secondaryBtn: {
    padding: "10px 18px",
    background: "#eee",
    color: "#111",
    border: "1px solid #ccc",
    borderRadius: 6,
    cursor: "pointer",
  },

  card: {
    background: "#fff",
    padding: 20,
    borderRadius: 10,
    border: "1px solid #ddd",
  },

  sectionTitle: {
    marginTop: 15,
  },

  // 🔥 THIS FIXES YOUR WHITE TEXT ISSUE COMPLETELY
  pre: {
    background: "#111",
    color: "#f5f5f5",
    padding: 12,
    borderRadius: 8,
    overflowX: "auto",
    fontSize: 13,
  },
};