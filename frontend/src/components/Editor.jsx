import { useCallback, useEffect, useRef, useState } from "react";
import { useEditor, EditorContent } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import Underline from "@tiptap/extension-underline";
import Placeholder from "@tiptap/extension-placeholder";
import { api } from "../api.js";
import Toolbar from "./Toolbar.jsx";
import ShareDialog from "./ShareDialog.jsx";

const AUTOSAVE_MS = 900;

export default function Editor({ docId, currentUser, onBack }) {
  const [doc, setDoc] = useState(null);
  const [title, setTitle] = useState("");
  const [status, setStatus] = useState("idle");
  const [loadError, setLoadError] = useState("");
  const [showShare, setShowShare] = useState(false);

  const saveTimer = useRef(null);
  const loadedOnce = useRef(false);

  const canEdit = doc && (doc.role === "owner" || doc.role === "edit");
  const isOwner = doc && doc.role === "owner";

  const editor = useEditor(
    {
      editable: false,
      extensions: [
        StarterKit.configure({ heading: { levels: [1, 2, 3] } }),
        Underline,
        Placeholder.configure({ placeholder: "Start writing…" }),
      ],
      content: "",
      onUpdate: ({ editor }) => {
        if (!loadedOnce.current) return;
        scheduleSave({ content: editor.getHTML() });
      },
    },
    [docId]
  );

  const doSave = useCallback(
    async (patch) => {
      setStatus("saving");
      try {
        const updated = await api.updateDocument(docId, patch);
        setDoc((d) => ({ ...d, ...updated }));
        setStatus("saved");
      } catch (err) {
        setStatus("error");
      }
    },
    [docId]
  );

  const scheduleSave = useCallback(
    (patch) => {
      setStatus("saving");
      if (saveTimer.current) clearTimeout(saveTimer.current);
      saveTimer.current = setTimeout(() => doSave(patch), AUTOSAVE_MS);
    },
    [doSave]
  );

  useEffect(() => {
    let cancelled = false;
    loadedOnce.current = false;
    setLoadError("");
    api
      .getDocument(docId)
      .then((d) => {
        if (cancelled) return;
        setDoc(d);
        setTitle(d.title);
        if (editor) {
          editor.commands.setContent(d.content || "<p></p>", false);
          editor.setEditable(d.role === "owner" || d.role === "edit");
        }
        setTimeout(() => {
          loadedOnce.current = true;
        }, 0);
        setStatus("saved");
      })
      .catch((err) => {
        if (!cancelled) setLoadError(err.detail || "Could not open document");
      });
    return () => {
      cancelled = true;
      if (saveTimer.current) clearTimeout(saveTimer.current);
    };
  }, [docId, editor]);

  function onTitleBlur() {
    const t = title.trim();
    if (!doc || t === doc.title) return;
    if (!t) {
      setTitle(doc.title);
      return;
    }
    doSave({ title: t });
  }

  const statusLabel = {
    idle: "",
    saving: "Saving…",
    saved: "All changes saved",
    error: "Save failed — retrying on next edit",
  }[status];

  if (loadError) {
    return (
      <div className="page">
        <header className="topbar">
          <button className="btn ghost" onClick={onBack}>
            Back
          </button>
        </header>
        <div className="container">
          <div className="error">{loadError}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <header className="topbar editor-topbar">
        <button className="btn ghost" onClick={onBack} title="Back to documents">
          Back
        </button>

        <input
          className="title-input"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          onBlur={onTitleBlur}
          onKeyDown={(e) => e.key === "Enter" && e.target.blur()}
          disabled={!canEdit}
          aria-label="Document title"
        />

        <div className="topbar-right">
          <span className={`save-status ${status}`}>{statusLabel}</span>
          {doc && !isOwner && (
            <span className="role-tag role-view" title="Your access level">
              {doc.role === "edit" ? "can edit" : "view only"}
            </span>
          )}
          {isOwner && (
            <button className="btn primary" onClick={() => setShowShare(true)}>
              Share
            </button>
          )}
        </div>
      </header>

      <Toolbar editor={editor} disabled={!canEdit} />

      <main className="editor-surface">
        <div className="editor-page">
          <EditorContent editor={editor} />
        </div>
      </main>

      {showShare && doc && (
        <ShareDialog
          doc={doc}
          onClose={() => setShowShare(false)}
          onChanged={() =>
            api.getDocument(docId).then((d) => setDoc((cur) => ({ ...cur, shares: d.shares })))
          }
        />
      )}
    </div>
  );
}
