import { useState } from "react";
import { analyzeEmail } from "./api";

const sampleEmails = [
  `Subject: Password Expiring Today
Your email password expires in 2 hours.
Reset now: http://microsoft-reset-secure.net/login`,

  `Subject: Urgent Account Verification Required
Your Microsoft 365 account has been flagged.
Verify here: http://security-check-login.net`,

  `Subject: Invoice Attached
Please review invoice attached and approve payment.`,

  `Subject: Suspicious Login Attempt
We detected a login from unknown device.`
];

export default function App() {
  const [email, setEmail] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const loadSample = () => {
    const random =
      sampleEmails[Math.floor(Math.random() * sampleEmails.length)];
    setEmail(random);
    setResult(null);
  };

  const analyze = async () => {
    try {
      setLoading(true);
      setResult(null);

      const data = await analyzeEmail(email);
      setResult(data);
    } catch (err) {
      setResult({ error: err.message });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.container}>
        <h1 style={styles.title}>🛡️ SOC Phishing Detection System</h1>

        <textarea
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Paste or load email..."
          style={styles.textarea}
        />

        <div style={styles.buttons}>
          <button style={styles.btn} onClick={loadSample}>
            Load Sample Email
          </button>

          <button style={styles.btnPrimary} onClick={analyze}>
            Analyze Email
          </button>
        </div>

        {loading && <p style={styles.loading}>Analyzing threat...</p>}

        {result && (
          <div style={styles.resultBox}>
            {result.error ? (
              <p style={{ color: "red" }}>{result.error}</p>
            ) : (
              <>
                <h2>
                  Verdict:{" "}
                  <span
                    style={{
                      color:
                        result.verdict === "phishing"
                          ? "red"
                          : "orange"
                    }}
                  >
                    {result.verdict}
                  </span>
                </h2>

                <p>Risk Score: {result.risk_score}</p>

                <h3>IOCs</h3>
                <ul>
                  {result.iocs?.map((ioc, i) => (
                    <li key={i}>{ioc}</li>
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

const styles = {
  page: {
    background: "linear-gradient(135deg, #0b1f3a, #071427)",
    minHeight: "100vh",
    color: "white",
    fontFamily: "Arial"
  },
  container: {
    maxWidth: "800px",
    margin: "0 auto",
    padding: "30px"
  },
  title: {
    fontSize: "26px",
    marginBottom: "20px"
  },
  textarea: {
    width: "100%",
    height: "180px",
    padding: "10px",
    borderRadius: "8px",
    border: "none"
  },
  buttons: {
    marginTop: "10px",
    display: "flex",
    gap: "10px"
  },
  btn: {
    padding: "10px",
    cursor: "pointer"
  },
  btnPrimary: {
    padding: "10px",
    background: "#2d6cdf",
    color: "white",
    border: "none",
    cursor: "pointer"
  },
  loading: {
    marginTop: "15px"
  },
  resultBox: {
    marginTop: "20px",
    padding: "15px",
    background: "#0f2a4d",
    borderRadius: "10px"
  }
};