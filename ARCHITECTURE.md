# Architecture note

A short account of what I built, the decisions behind it, and what I
deliberately left out under the timebox.

## What I prioritized

The brief rewards **depth in a few areas over shallow coverage everywhere**, so
I spent my time on the three things that are hardest to fake and easiest to get
subtly wrong:

1. **A real editing experience** — not a `<textarea>`. TipTap gives genuine
   rich text (bold/italic/underline, H1–H3, bullet/ordered lists, undo/redo)
   with clean HTML output, plus autosave so nothing is lost.
2. **Correct, server-enforced sharing** — ownership and `view`/`edit` roles are
   checked on every endpoint through one `access.py` module, not scattered `if`
   statements. The UI distinction ("My documents" vs "Shared with me") is driven
   by the same server-computed role.
3. **Trustworthy handling of untrusted content** — all HTML (from the editor and
   from uploaded `.docx`/`.md` files) is sanitized through an allow-list before
   storage, closing the obvious stored-XSS hole.

## System shape

```
Browser (React + TipTap SPA)
      │  fetch /api/*  (JWT bearer)
      ▼
FastAPI  ──►  routers/auth.py        login, /me
         ──►  routers/documents.py   CRUD, upload, sharing
                    │
          access.py (role checks) · sanitize.py (XSS) · file_import.py (uploads)
                    ▼
            SQLAlchemy ORM  ──►  SQLite (or Postgres via DATABASE_URL)
```

In production a **single FastAPI process** serves both the JSON API (`/api/*`)
and the built React bundle (everything else), so the product deploys as one
container with no CORS or multi-service orchestration. In local dev the SPA runs
on Vite and proxies `/api` to the backend.

## Key decisions & tradeoffs

| Decision | Why | Tradeoff / what I gave up |
|---|---|---|
| **TipTap** for the editor | Battle-tested ProseMirror core; gives real rich text fast and emits clean, sanitizable HTML | Larger JS bundle than a hand-rolled editor |
| **HTML (not JSON) as the stored format** | Renders directly, easy to sanitize, trivial to export later | Slightly less structured than ProseMirror JSON for future diffing |
| **SQLite by default, Postgres-ready** | Zero-setup for reviewers (`pip install` and go); swapping to Postgres is a one-line `DATABASE_URL` change (psycopg already included) | SQLite isn't ideal for high-concurrency writes |
| **Seeded demo users + JWT, no sign-up** | The brief explicitly allows seeded/mocked auth; this keeps the sharing demo frictionless while still being *real* (hashed passwords, signed tokens, enforced server-side) | No registration or password reset |
| **Autosave via debounced PATCH** | Feels like Docs; avoids a "Save" button and lost work | Not real-time multi-user sync (see below) |
| **Centralized `access.py`** | One place defines owner/edit/view semantics → consistent + testable | — |
| **Return 404 (not 403) for docs you can't see** | Doesn't leak which document IDs exist | — |

## Access-control model

- **Owner**: full control — edit, rename, share/unshare, delete.
- **Edit** (shared): edit content + rename. Cannot delete or manage sharing.
- **View** (shared): read-only.
- **No access**: the document returns 404.

This is simple on purpose — the brief says it "does not need to be
enterprise-grade" — but it is enforced on the server for every action, so the
client cannot bypass it.

## Data model

- `User(id, email, name, password_hash)`
- `Document(id, title, content, owner_id, created_at, updated_at)`
- `Share(document_id, user_id, permission)` — unique per (document, user)

## Quality & reliability

- **Validation**: Pydantic schemas validate every request body; uploads are
  size-checked and type-checked, with clean error messages surfaced in the UI.
- **Security**: passwords hashed (pbkdf2_sha256); JWT-signed sessions; all
  stored HTML sanitized against an allow-list.
- **Tests**: `backend/tests/test_api.py` — 8 cases concentrated on the
  highest-risk logic (sharing permissions, upload conversion, sanitization)
  rather than trivial getters. Run with `pytest -q`.

## Explicitly out of scope (and why)

- **Real-time collaborative cursors / CRDT sync.** The highest-effort,
  highest-risk feature; the brief lists it only as optional stretch. Autosave +
  reopen covers the core "collaborate on shared work" need within the timebox.
- **Full auth** (sign-up, email verification, password reset) — the brief
  permits seeded accounts, so this would be effort spent away from the graded
  core.
- **Granular/role-based permissions beyond view/edit** — listed as optional
  stretch.
- **Document version history & PDF export** — optional stretch; the HTML storage
  format makes both straightforward to add later.

## What I'd build next (with another 2–4 hours)

1. **Live presence + real-time sync** via a WebSocket broadcasting ProseMirror
   steps (or Yjs) — the natural next step for a "collaborative" editor.
2. **Export to PDF / Markdown** — easy given HTML storage.
3. **Document version history** — snapshot on save; diff view.
4. **Sign-up flow** so it isn't limited to seeded users.
5. **E2E test** (Playwright) covering the share → sign-in-as-other-user path end
   to end, complementing the API tests.
