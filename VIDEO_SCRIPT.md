# Walkthrough video script (3–5 min)

Record with Loom (easiest — screen + mic) against your live URL or
`http://localhost:8000`. Aim for ~4 minutes. Outline below; speak to it, don't
read it verbatim.

---

### 0:00 — Intro (20s)
"Hi, I'm Meghana. This is CollabDocs, a lightweight collaborative document
editor I built for this assignment. Stack is FastAPI, React with the TipTap
editor, and SQLAlchemy with SQLite, deployed as a single Docker container. Let
me walk through the main flow."

### 0:20 — Create + edit (60s)
- Log in as **alice@example.com**.
- Click **New document**. Rename it (click the title).
- Type a heading, some text. Use the toolbar: **bold, italic, underline, H1/H2,
  bullet and numbered lists.**
- Point out **"All changes saved"** — "edits autosave; no save button, nothing
  gets lost."
- Refresh the page → "formatting and content persist."

### 1:20 — File upload (40s)
- Back to dashboard → **Upload file**.
- Pick a `.md` or `.docx` file → "it's converted to a fully editable rich-text
  document — headings, bold, lists all come through. Supported types are stated
  in the UI; unsupported ones are rejected with a clear error."

### 2:00 — Sharing (70s) — the core
- Open a doc → **Share** → add `carol@example.com` as **Can edit**.
- "Sharing is role-based: view or edit. Ownership and roles are enforced on the
  server, not just hidden in the UI."
- Sign out → sign in as **carol@example.com**.
- "The document now shows under **Shared with me**, separate from documents I
  own, with its role badge. I can edit the content but not delete it — only the
  owner can."

### 3:10 — Engineering + what I cut (45s)
- Show `pytest -q` → "8 tests, focused on the risky logic: sharing permissions
  and sanitizing untrusted uploaded content. In fact a test caught a real bug —
  the email validator rejected my seeded domain — which I only found by running
  them."
- "I deliberately cut real-time collaborative cursors. That's the highest-risk
  feature and only optional in the brief; I prioritized a solid editing +
  sharing core instead. Next I'd add WebSocket sync and PDF export."

### 3:55 — AI usage (30s)
- "I used Claude Code to scaffold the full stack and draft tests, which let me
  spend my time on judgment calls — scope, the data model, and adding HTML
  sanitization for security. I verified everything by running the tests and
  clicking through the app; I didn't trust generated code until it ran."

### 4:25 — Wrap (10s)
"That's CollabDocs — code, README, architecture and AI notes are all in the
repo. Thanks for watching."

---

**Tips**
- Have the app open and logged in as Alice before you hit record.
- Have a sample `.md`/`.docx` file on your desktop ready to upload.
- If anything misbehaves live, just narrate it — reviewers value honesty about
  tradeoffs over a flawless take.
