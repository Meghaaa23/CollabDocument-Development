# AI-native workflow note

> This is an AI-forward role, so here is an honest account of how I used AI on
> this assignment — where it helped, where I overrode it, and how I kept
> engineering judgment in my own hands rather than outsourcing it.

## Tools used

- **Claude (Claude Code / Opus, in the Claude desktop app)** — my primary
  pair-programmer: scaffolding the FastAPI + React app, generating boilerplate
  (ORM models, Pydantic schemas, CSS), drafting tests and docs, and driving a
  browser to verify the running app.
- Standard local tooling (`pytest`, `uvicorn`, `vite`) for ground-truth
  verification — I never trusted AI output until I ran it.

## Where AI materially sped me up

- **Scaffolding the full stack.** The repetitive, well-understood layers —
  SQLAlchemy models, request/response schemas, the fetch client, the CSS design
  system, the Dockerfile — are where AI is strongest. Generating these in
  minutes freed my time for the decisions that actually matter.
- **The TipTap toolbar + autosave wiring** — correct but fiddly glue code
  (keeping editor focus on toolbar clicks, debouncing saves, not firing a save
  during the initial `setContent`).
- **Test and doc drafts** — AI produced first drafts of the pytest cases and
  this documentation, which I then shaped to match the real priorities.

## What I changed or rejected

- **I directed the architecture, not the AI.** The decisions that shape the
  product were mine: *what* to build deeply vs. cut (real-time sync → out of
  scope), HTML-vs-JSON storage, SQLite-with-a-Postgres-escape-hatch, returning
  404 instead of 403 to avoid leaking document existence, and centralizing all
  access control in one `access.py` module. AI implemented these; it didn't
  choose them.
- **I added the security layer AI didn't volunteer.** Stored content comes from
  an untrusted client *and* from uploaded `.docx` files, so I insisted on an
  allow-list HTML sanitizer (`sanitize.py`) to close the stored-XSS hole. There
  is a test proving a `<script>` tag is stripped on save.
- **I kept the test suite focused.** Rather than a pile of trivial assertions, I
  concentrated coverage on the highest-risk logic: sharing permissions (a viewer
  must not edit/delete; an unshared user gets 404) and untrusted-content
  handling.

## How I verified correctness, UX, and reliability

- **Tests caught a real bug.** The first `pytest` run failed: the Pydantic
  `EmailStr` validator rejects `.test` domains (a reserved TLD), so logins
  returned 422. I would not have caught this by eye. I switched the seeded
  accounts to `@example.com` and the suite went green (8/8). This is the whole
  point of not trusting generated code blindly.
- **Manual end-to-end check in a browser.** I ran the production single-service
  build (FastAPI serving the built SPA) and clicked through the real flows:
  login → dashboard (owned vs. shared split) → open doc → verify rich-text
  rendering and autosave → **Share** with another user → confirmed the grant
  appears with the right role. Screenshots are in `docs/screenshots/`.
- **Reliability**: input validation on every endpoint, size/type limits on
  uploads, typed HTTP errors surfaced in the UI, and a `/api/health` check for
  the deploy platform.

## Principle I worked by

AI is excellent at *execution* and weak at *judgment under ambiguity*. I used it
to move fast on the former and reserved the latter — scope, security, data
model, what to cut — for myself. The assignment asked for "practical AI usage,
not volume," and the tell is this: the one bug that mattered was caught by a
test I ran, not by the model that wrote the code.
