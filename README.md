# CollabDocs

A lightweight collaborative document editor (Google Docs–inspired), built as a
timeboxed full-stack take-home. Users can create, edit, rename, upload, and
**share** rich-text documents, with ownership and access enforced server-side.

**Live demo:** https://collabdocs-untf.onrender.com — sign in as
`alice@example.com` / `demo1234`. _(Free tier: first load after idle can take
~30–50s to wake.)_

**Stack:** FastAPI (Python) · React + Vite · TipTap editor · SQLAlchemy + SQLite
(Postgres-ready) · JWT auth · Docker single-image deploy.

---

## Feature checklist

| Requirement | Status | Notes |
|---|---|---|
| Create / rename / edit / save / reopen | Done | Autosave (debounced) + explicit "All changes saved" status |
| Rich text: bold, italic, underline, headings, lists | Done | TipTap toolbar; content stored as sanitized HTML |
| File upload → editable doc | Done | `.txt`, `.md`, `.docx` converted to rich text (`mammoth` / Markdown) |
| Sharing (owner + grant + owned/shared distinction) | Done | `view` / `edit` roles; "My documents" vs "Shared with me" |
| Persistence across refresh | Done | SQLite (swap to Postgres via one env var) |
| Validation & error handling | Done | Pydantic validation, typed HTTP errors, HTML sanitization (XSS defense) |
| Automated test | Done | 8 pytest cases focused on access control + untrusted content |
| Architecture note | Done | [`ARCHITECTURE.md`](./ARCHITECTURE.md) |
| AI workflow note | Done | [`AI_WORKFLOW.md`](./AI_WORKFLOW.md) |
| Live deployment | Done | Live at https://collabdocs-untf.onrender.com (single Docker image on Render) |

---

## Quick start (local)

Prereqs: **Python 3.11+** and **Node 18+**.

You need two terminals — one for the API, one for the SPA.

### 1. Backend (terminal 1)

```bash
cd backend
python -m venv .venv
# Windows:        .venv\Scripts\activate
# macOS / Linux:  source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API now at http://localhost:8000 (docs at http://localhost:8000/docs).
The database file and demo data are created automatically on first run.

### 2. Frontend (terminal 2)

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173**. The Vite dev server proxies `/api` to the
backend, so no extra configuration is needed.

### Demo accounts

All use password **`demo1234`**:

| Email | Role in the demo |
|---|---|
| `alice@example.com` | Owns the two seeded sample documents |
| `bob@example.com` | Already has a document shared with him (edit) |
| `carol@example.com` | Starts empty — share a doc *to* her to demo the flow |

> To demo sharing: log in as Alice → open a doc → **Share** → add
> `bob@example.com` or `carol@example.com` → sign out → log in as that user →
> see it under **Shared with me**.

---

## Run tests

```bash
cd backend
pip install -r requirements.txt   # includes pytest + httpx
pytest -q
```

Expected: `8 passed`.

---

## Run as a single service (production shape)

FastAPI can serve the built SPA itself, so the whole product runs as one
process. This is exactly what the Docker image does.

```bash
# build the SPA and drop it where the backend serves it
cd frontend && npm install && npm run build && cd ..
#  copy frontend/dist -> backend/static  (Windows PowerShell shown)
#  macOS/Linux:  cp -r frontend/dist backend/static
powershell -c "Copy-Item -Recurse -Force frontend/dist backend/static"

cd backend
uvicorn app.main:app --port 8000
# open http://localhost:8000  (API + UI from one origin)
```

---

## Deploy

The repo ships a **single Dockerfile** that builds the frontend and serves
everything from FastAPI, so it deploys to any container host.

### Option A — Render (free, recommended; uses the included `render.yaml`)

1. Push this repo to GitHub.
2. Render dashboard → **New + → Blueprint** → select the repo. It reads
   `render.yaml` and provisions a free Docker web service with a generated
   `JWT_SECRET` and a `/api/health` health check.
3. Deploy. Your live URL is `https://collabdocs-XXXX.onrender.com`.

> Free Render instances have an ephemeral disk, so the SQLite file resets on
> restart — the demo data **re-seeds automatically** every boot, so the live app
> is always testable. For durable storage, create a free Postgres DB (Render or
> [Neon](https://neon.tech)) and set `DATABASE_URL` to its
> `postgresql+psycopg://…` URL. No code changes needed.

### Option B — any Docker host (Railway, Fly.io, Cloud Run, a VPS)

```bash
docker build -t collabdocs .
docker run -p 8000:8000 -e JWT_SECRET=$(openssl rand -hex 32) collabdocs
# open http://localhost:8000
```

Set `JWT_SECRET` (required in prod) and optionally `DATABASE_URL`. The container
listens on `$PORT` (default 8000).

---

## Project layout

```
backend/
  app/
    main.py          FastAPI app, CORS, SPA serving, startup seed
    config.py        env-driven settings
    database.py      SQLAlchemy engine/session
    models.py        User, Document, Share
    schemas.py       Pydantic request/response + validation
    security.py      password hashing + JWT auth
    access.py        centralized document access-control rules
    sanitize.py      HTML allow-list sanitizer (XSS defense)
    file_import.py   .txt / .md / .docx -> rich-text HTML
    seed.py          demo users + sample documents
    routers/
      auth.py        /api/auth/*
      documents.py   /api/documents/* (CRUD, upload, sharing)
  tests/test_api.py  pytest suite
frontend/
  src/
    App.jsx          view routing + auth bootstrap
    api.js           fetch client
    components/      Login, Dashboard, Editor, Toolbar, ShareDialog
    styles.css
Dockerfile           two-stage single-image build
render.yaml          Render blueprint
docs/screenshots/    UI screenshots
```

See [`SUBMISSION.md`](./SUBMISSION.md) for the full deliverable index, what is
intentionally out of scope, and what I'd build next.
