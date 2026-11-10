# CollabDocs — AI-Native Full Stack Developer Assignment

**Candidate:** Meghana Konka
**Live app:** https://collabdocs-untf.onrender.com
**Source:** https://github.com/Meghaaa23/CollabDocument-Development
**Walkthrough video:** [PASTE YOUR LOOM/YOUTUBE LINK]
**Google Drive folder:** [PASTE YOUR DRIVE FOLDER LINK]

A lightweight, Google Docs–inspired collaborative document editor. I prioritized
depth in a few areas over shallow coverage, with deliberate scope cuts explained
below.

> **Demo logins** (password `demo1234`):
> `alice@example.com` (owns sample docs) · `bob@example.com` (has a doc shared
> with him) · `carol@example.com` (empty).
> _Free Render tier: the first request after idle can take ~30–50s to wake._

## What it does (mapped to the brief)

| Requirement | Status |
|---|---|
| Create / rename / edit / save / reopen documents | Autosave + "All changes saved" status |
| Rich text: bold, italic, underline, headings, lists | TipTap editor; stored as sanitized HTML |
| File upload → editable document | `.txt` / `.md` / `.docx` converted to rich text |
| Sharing (owner + grant access + owned vs shared) | `view` / `edit` roles; "My documents" vs "Shared with me" |
| Persistence across refresh | SQLite (one env var swaps to Postgres) |
| Validation + error handling | Pydantic validation, typed errors, HTML sanitization (XSS defense) |
| Automated test | 8 pytest cases (sharing permissions + untrusted content) |
| Live deployment | Single Docker image on Render |

## Review the sharing flow in 30 seconds

1. Sign in as **alice@example.com**.
2. Open **"Welcome to CollabDocs"** → **Share** → add `carol@example.com`.
3. Sign out → sign in as **carol@example.com** → it appears under **"Shared with
   me"** (not "My documents"), with its role badge. A viewer can't delete it; an
   editor can edit content but still can't delete — all enforced server-side.

## Stack & architecture

- **Backend:** FastAPI + SQLAlchemy (SQLite, Postgres-ready), JWT auth.
- **Frontend:** React + Vite with the TipTap rich-text editor.
- **One service in production:** FastAPI serves both the JSON API (`/api/*`) and
  the built React SPA, so the whole product deploys as a single Docker container.
- **Access control** is centralized in one module and enforced on every endpoint
  (owner → full control; edit → content + rename; view → read-only; no access →
  404 so document existence isn't leaked).
- **Security:** all stored HTML (from the editor *and* uploaded `.docx`/`.md`
  files) is passed through an allow-list sanitizer to prevent stored XSS.

Full reasoning is in `ARCHITECTURE.md` in the repo/Drive folder.

## AI-native workflow (summary)

I used **Claude (Claude Code)** to scaffold the full stack, generate boilerplate,
and draft tests/docs — then reserved the judgment calls for myself: scope (cut
real-time sync), the data model, returning 404 vs 403, and adding the HTML
sanitization layer for security. I verified everything by running the tests and
clicking through the live app; I didn't trust generated code until it ran. A test
even caught a real bug (the email validator rejected my seeded domain), which I
only found by running the suite — the point of using AI *with* judgment, not
instead of it. Details in `AI_WORKFLOW.md`.

## Scope cuts (deliberate)

- **No real-time multi-user sync / live cursors** — highest effort/risk, only an
  optional stretch in the brief. Collaboration is via share + autosave + reopen.
- **Seeded accounts, no sign-up** — allowed by the brief; keeps the sharing demo
  frictionless.
- Version history, PDF export, granular roles — optional stretch, not built.

## What I'd build next (another 2–4 hours)

1. Real-time sync (WebSocket broadcasting editor steps, or Yjs).
2. Export to PDF / Markdown (easy given HTML storage).
3. Document version history with a diff view.
4. A Playwright end-to-end test for the cross-user sharing path.
