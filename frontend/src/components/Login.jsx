import { useState } from "react";
import { api } from "../api.js";

const DEMO_ACCOUNTS = [
  { email: "alice@example.com", label: "Alice (owns the sample docs)" },
  { email: "bob@example.com", label: "Bob (a doc is shared with him)" },
  { email: "carol@example.com", label: "Carol (no docs yet)" },
];

export default function Login({ onLoggedIn }) {
  const [email, setEmail] = useState("alice@example.com");
  const [password, setPassword] = useState("demo1234");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(e) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      const res = await api.login(email.trim(), password);
      onLoggedIn(res.access_token, res.user);
    } catch (err) {
      setError(err.detail || "Login failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="centered">
      <form className="card login-card" onSubmit={submit}>
        <h1 className="brand">CollabDocs</h1>
        <p className="muted">Lightweight collaborative document editor</p>

        <label>Email</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          autoComplete="username"
          required
        />

        <label>Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          autoComplete="current-password"
          required
        />

        {error && <div className="error">{error}</div>}

        <button className="btn primary" type="submit" disabled={busy}>
          {busy ? "Signing in…" : "Sign in"}
        </button>

        <div className="demo-box">
          <div className="muted small">Demo accounts (password: <code>demo1234</code>)</div>
          {DEMO_ACCOUNTS.map((a) => (
            <button
              type="button"
              key={a.email}
              className="demo-pill"
              onClick={() => {
                setEmail(a.email);
                setPassword("demo1234");
              }}
            >
              {a.label}
            </button>
          ))}
        </div>
      </form>
    </div>
  );
}
