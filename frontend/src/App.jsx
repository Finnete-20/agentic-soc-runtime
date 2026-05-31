import { useState } from "react";

const API_URL =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8000";

export default function App() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  // -------------------------------
  // RANDOM SAMPLE EMAILS
  // -------------------------------
  const samples = [
    {
      type: "phishing",
      content: `Subject: Urgent Account Verification Required

Dear User,

Your Microsoft 365 account has been flagged for suspicious activity.

To avoid suspension, verify immediately:
http://security-verification-login.com

IT Security Team`
    },
    {
      type: "banking",
      content: `Subject: Bank Account Locked

We detected unusual activity on your account.

Confirm your identity immediately:
http://secure-bank-login-update.com

Failure will permanently suspend your account.`
    },
    {
      type: "password_reset",
      content: `Subject: Password Expiring Today

Your password expires in 2 hours.

Reset now:
http://password-reset-security.com

IT Support Desk`
    },
    {
      type: "delivery",
      content: `Subject: Package Delivery Failed

We could not deliver your package.

Reschedule delivery here:
http://delivery-reschedule-service.com`
    },
    {
      type: "hr_scam",
      content: `Subject: Payroll Update Required

HR Department:

Please confirm your payroll details to avoid salary delay.

Update here:
http://hr-payroll-update.com`
    }
  ];

  // RANDOM SAMPLE GENERATOR
  const loadSample = () => {
    const randomIndex = Math.floor(Math.random() * samples.length);
    setEmail(samples[randomIndex].content);
  };

  // -------------------------------
  // ANALYZE EMAIL
  // -------------------------------
  const analyzeEmail = async () => {
    if (!email.trim()) {
      alert("Please enter or load an email first.");
      return;
    }

    setLoading(true);
    setResult(null);

    try {
      const res = await fetch(`${API_URL}/investigate`, {
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

  // -------------------------------
  // UI
  // -------------------------------
  return (
    <div style={styles.page}>
      <h1 style={styles.title}>SOC Phishing Detection System</h1>

      <p style={styles.subtitle}>
        AI-powered email threat analysis & SOC investigation engine
      </p>

      <textarea
        style={styles.textarea}
        placeholder="Paste email content here..."
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />

      <div style={styles.buttonRow}>
        <button style={styles.sampleButton} onClick={loadSample}>
          Load Sample Email
        </button>

        <button style={styles.button} onClick={analyzeEmail}>
          {loading ? "Analyzing..." : "Analyze Email"}
        </button>
      </div>

      {result && (
        <div style={styles.card}>
          <h2 style={styles.heading}>Result</h2>

          <p><strong>Verdict:</strong> {result.verdict}</p>

          <p>
            <strong>Risk Score:</strong>{" "}
            {result.risk_score?.toFixed?.(2)}
          </p>

          <h3 style={styles.heading}>IOC Features</h3>
          <pre style={styles.code}>
            {JSON.stringify(result.iocs, null, 2)}
          </pre>

          <h3 style={styles.heading}>Threat Data</h3>
          <pre style={styles.code}>
            {JSON.stringify(result.threat_data, null, 2)}
          </pre>

          <h3 style={styles.heading}>Investigation Steps</h3>
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

// -------------------------------
// STYLES (DARK SOC DASHBOARD)
// -------------------------------
const styles = {
  page: {
    fontFamily: "Arial",
    padding: "30px",
    maxWidth: "900px",
    margin: "0 auto",
    backgroundColor: "#0b1220",
    minHeight: "100vh",
    color: "white",
  },

  title: {
    textAlign: "center",
    marginBottom: "5px",
  },

  subtitle: {
    textAlign: "center",
    color: "#94a3b8",
    marginBottom: "20px",
  },

  textarea: {
    width: "100%",
    height: "180px",
    padding: "12px",
    fontSize: "14px",
    marginBottom: "15px",
    borderRadius: "8px",
    border: "1px solid #334155",
    backgroundColor: "#111827",
    color: "white",
  },

  buttonRow: {
    display: "flex",
    gap: "10px",
    marginBottom: "20px",
    flexWrap: "wrap",
  },

  button: {
    padding: "10px 20px",
    backgroundColor: "#111827",
    color: "white",
    border: "1px solid #334155",
    borderRadius: "8px",
    cursor: "pointer",
  },

  sampleButton: {
    padding: "10px 20px",
    backgroundColor: "#2563eb",
    color: "white",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
  },

  card: {
    border: "1px solid #334155",
    borderRadius: "10px",
    padding: "20px",
    backgroundColor: "#0f172a",
    marginTop: "20px",
  },

  heading: {
    color: "white",
  },

  code: {
    backgroundColor: "#1e293b",
    padding: "10px",
    borderRadius: "5px",
    overflowX: "auto",
    color: "white",
  },
};