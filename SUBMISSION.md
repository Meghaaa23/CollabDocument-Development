# SUBMISSION

**Project:** CollabDocs — a lightweight collaborative document editor
**Candidate:** Meghana Konka
**Stack:** FastAPI · React + Vite · TipTap · SQLAlchemy/SQLite · Docker

---

## What is included

| Item | Location |
|---|---|
| Source code (backend + frontend) | `backend/`, `frontend/` |
| Local setup & run instructions | [`README.md`](./README.md) |
| Architecture note | [`ARCHITECTURE.md`](./ARCHITECTURE.md) |
| AI workflow note | [`AI_WORKFLOW.md`](./AI_WORKFLOW.md) |
| Automated tests (8 passing) | `backend/tests/test_api.py` |
| Dockerfile + Render blueprint | `Dockerfile`, `render.yaml` |
| UI screenshots | `docs/screenshots/` |
| Walkthrough video link | `VIDEO_LINK.txt` |
| This index | `SUBMISSION.md` |

## Live deployment

- **Live URL:** **https://collabdocs-untf.onrender.com**
  - _Hosted on Render's free tier; the first request after idle can take ~30–50s to wake (cold start), then it's fast._
- **Demo accounts** (password `demo1234`):
  - `alice@example.com` — owns the sample documents
  - `bob@example.com` — has a document shared with him
  - `carol@example.com` — empty; share a doc to her to demo the flow

## How to review the sharing flow quickly

1. Sign in as **alice@example.com**.
2. Open **“Welcome to CollabDocs”** → click **Share** → add `carol@example.com`.
3. Sign out → sign in as **carol@example.com** → the doc appears under
   **“Shared with me”** (not “My documents”), with its role badge.
4. As Carol (view role) you cannot delete it; as an edit-share you can edit the
   content but still cannot delete — all enforced server-side.

## What is working (end to end)

- Create, rename, edit, save (autosave), and reopen documents
- Rich text: bold, italic, underline, H1–H3, bullet & numbered lists, undo/redo
- Upload `.txt` / `.md` / `.docx` → new editable document
- Share with another user (view/edit); owned vs. shared clearly distinguished
- Persistence across refresh; formatting preserved
- Input validation, error handling, HTML sanitization (XSS defense)
- 8 automated tests passing (`pytest -q`)

## What is incomplete / intentionally out of scope

- **Real-time multi-user sync / live cursors** — optional stretch; highest
  effort/risk. Collaboration is via share + autosave + reopen.
- Sign-up / password reset — seeded accounts used (allowed by the brief).
- Version history, PDF export, granular roles — optional stretch.

## What I'd build next (another 2–4 hours)

1. Real-time sync (WebSocket broadcasting editor steps, or Yjs).
2. Export to PDF / Markdown (easy given HTML storage).
3. Document version history with a diff view.
4. A Playwright E2E test covering the cross-user sharing path.

_(Full reasoning in [`ARCHITECTURE.md`](./ARCHITECTURE.md).)_
