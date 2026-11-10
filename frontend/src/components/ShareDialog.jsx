import { useState } from "react";
import { api } from "../api.js";

export default function ShareDialog({ doc, onClose, onChanged }) {
  const [shares, setShares] = useState(doc.shares || []);
  const [email, setEmail] = useState("");
  const [permission, setPermission] = useState("edit");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function addShare(e) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      const share = await api.addShare(doc.id, email.trim(), permission);
      setShares((prev) => {
        const rest = prev.filter((s) => s.user.id !== share.user.id);
        return [...rest, share];
      });
      setEmail("");
      onChanged?.();
    } catch (err) {
      setError(err.detail || "Could not share");
    } finally {
      setBusy(false);
    }
  }

  async function revoke(userId) {
    setBusy(true);
    try {
      await api.removeShare(doc.id, userId);
      setShares((prev) => prev.filter((s) => s.user.id !== userId));
      onChanged?.();
    } catch (err) {
      setError(err.detail || "Could not revoke");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-head">
          <h3>Share “{doc.title}”</h3>
          <button className="btn ghost" onClick={onClose} title="Close">
            Close
          </button>
        </div>

        <form className="share-form" onSubmit={addShare}>
          <input
            type="email"
            placeholder="person@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
          <select value={permission} onChange={(e) => setPermission(e.target.value)}>
            <option value="edit">Can edit</option>
            <option value="view">Can view</option>
          </select>
          <button className="btn primary" type="submit" disabled={busy}>
            Share
          </button>
        </form>
        <div className="muted small">
          Tip: try <code>bob@example.com</code> or <code>carol@example.com</code>.
        </div>

        {error && <div className="error">{error}</div>}

        <div className="share-list">
          <div className="muted small">People with access</div>
          <div className="share-row owner-row">
            <span>{doc.owner.name} ({doc.owner.email})</span>
            <span className="role-tag role-owner">owner</span>
          </div>
          {shares.length === 0 && (
            <div className="muted small">Not shared with anyone yet.</div>
          )}
          {shares.map((s) => (
            <div className="share-row" key={s.user.id}>
              <span>
                {s.user.name} ({s.user.email})
              </span>
              <span className="share-row-right">
                <span className={`role-tag role-${s.permission}`}>{s.permission}</span>
                <button
                  className="link-btn danger"
                  onClick={() => revoke(s.user.id)}
                  disabled={busy}
                >
                  remove
                </button>
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
