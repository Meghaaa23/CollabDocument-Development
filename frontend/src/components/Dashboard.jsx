import { useEffect, useRef, useState } from "react";
import { api } from "../api.js";

function formatDate(iso) {
  try {
    return new Date(iso).toLocaleString();
  } catch {
    return iso;
  }
}

function DocCard({ doc, onOpen, onDelete }) {
  return (
    <div className="doc-card" onClick={() => onOpen(doc.id)}>
      <div className="doc-card-body">
        <div className="doc-title">{doc.title || "Untitled document"}</div>
        <div className="muted small">
          {doc.is_owner ? "You own this" : `Shared by ${doc.owner.name}`} ·{" "}
          <span className={`role-tag role-${doc.role}`}>{doc.role}</span>
        </div>
        <div className="muted small">Updated {formatDate(doc.updated_at)}</div>
      </div>
      {doc.is_owner && (
        <button
          className="link-btn danger"
          title="Delete document"
          onClick={(e) => {
            e.stopPropagation();
            onDelete(doc);
          }}
        >
          Delete
        </button>
      )}
    </div>
  );
}

export default function Dashboard({ currentUser, onOpenDoc, onLogout }) {
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const fileInput = useRef(null);

  async function load() {
    setLoading(true);
    setError("");
    try {
      setDocs(await api.listDocuments());
    } catch (err) {
      setError(err.detail || "Could not load documents");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function createNew() {
    setBusy(true);
    try {
      const doc = await api.createDocument("Untitled document", "<p></p>");
      onOpenDoc(doc.id);
    } catch (err) {
      setError(err.detail || "Could not create document");
    } finally {
      setBusy(false);
    }
  }

  async function handleUpload(e) {
    const file = e.target.files?.[0];
    e.target.value = "";
    if (!file) return;
    setBusy(true);
    setError("");
    try {
      const doc = await api.uploadDocument(file);
      onOpenDoc(doc.id);
    } catch (err) {
      setError(err.detail || "Upload failed");
    } finally {
      setBusy(false);
    }
  }

  async function handleDelete(doc) {
    if (!window.confirm(`Delete "${doc.title}"? This cannot be undone.`)) return;
    try {
      await api.deleteDocument(doc.id);
      setDocs((d) => d.filter((x) => x.id !== doc.id));
    } catch (err) {
      setError(err.detail || "Delete failed");
    }
  }

  const owned = docs.filter((d) => d.is_owner);
  const shared = docs.filter((d) => !d.is_owner);

  return (
    <div className="page">
      <header className="topbar">
        <div className="brand small-brand">CollabDocs</div>
        <div className="topbar-right">
          <span className="muted small">
            {currentUser.name} ({currentUser.email})
          </span>
          <button className="btn ghost" onClick={onLogout}>
            Sign out
          </button>
        </div>
      </header>

      <main className="container">
        <div className="actions-row">
          <button className="btn primary" onClick={createNew} disabled={busy}>
            New document
          </button>
          <button
            className="btn"
            onClick={() => fileInput.current?.click()}
            disabled={busy}
          >
            Upload file
          </button>
          <input
            ref={fileInput}
            type="file"
            accept=".txt,.md,.markdown,.docx"
            style={{ display: "none" }}
            onChange={handleUpload}
          />
          <span className="muted small upload-hint">
            Supported: .txt, .md, .docx becomes an editable doc
          </span>
        </div>

        {error && <div className="error">{error}</div>}
        {loading && <div className="muted">Loading documents…</div>}

        {!loading && (
          <>
            <section>
              <h2 className="section-title">My documents</h2>
              {owned.length === 0 ? (
                <p className="muted">No documents yet. Create or upload one above.</p>
              ) : (
                <div className="doc-grid">
                  {owned.map((d) => (
                    <DocCard key={d.id} doc={d} onOpen={onOpenDoc} onDelete={handleDelete} />
                  ))}
                </div>
              )}
            </section>

            <section>
              <h2 className="section-title">Shared with me</h2>
              {shared.length === 0 ? (
                <p className="muted">Nothing shared with you yet.</p>
              ) : (
                <div className="doc-grid">
                  {shared.map((d) => (
                    <DocCard key={d.id} doc={d} onOpen={onOpenDoc} onDelete={handleDelete} />
                  ))}
                </div>
              )}
            </section>
          </>
        )}
      </main>
    </div>
  );
}
