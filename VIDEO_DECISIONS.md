# Video talking points - decisions and why

Speak these in your own words. Each is one or two sentences. Total ~2 minutes;
weave them in while clicking through, or say them as a "decisions" segment.

## Opening line (the philosophy)
"The brief rewards deliberate scope cuts over trying to clone Google Docs, so my
whole approach was: pick a few things that are hard to get right, build those
properly, and cut the rest on purpose."

## The decisions

Scope - I cut real-time sync.
"Live multi-user cursors are the highest-effort, highest-risk feature and only an
optional stretch, so I cut them and spent the time on a solid editing and sharing
core instead. Collaboration here is share + autosave + reopen."

Stack - FastAPI + React + TipTap.
"FastAPI gives me typed request validation basically for free, React keeps the UI
in simple components, and TipTap gives me a real rich-text editor without building
one from scratch - and it outputs clean HTML I can store and sanitize."

One service instead of two.
"In production, FastAPI serves both the API and the built React app, so the whole
thing deploys as a single Docker container - no CORS juggling, no two-service
orchestration. That's why it was a 4-minute deploy."

SQLite by default, Postgres-ready.
"I used SQLite so a reviewer can clone and run it with zero database setup, but
it's one environment variable to switch to Postgres - so it's convenient now and
production-ready later."

I store the document as HTML, not JSON.
"HTML renders directly, it's trivial to sanitize, and it makes export to PDF or
Markdown easy later - a small decision that keeps future options open."

All access control lives in one module.
"Owner, edit, and view permissions are defined in one place and enforced on every
endpoint, so the rules are consistent and easy to test - not scattered if-checks."

I return 404, not 403, for documents you can't see.
"If you don't have access, the API says 'not found' rather than 'forbidden', so it
never even leaks that a document exists. Small thing, but it's the right default."

I sanitize all HTML before storing it.
"Content comes from an untrusted browser and from uploaded Word files, so I run
all of it through an allow-list sanitizer to prevent stored XSS - and there's a
test proving a script tag gets stripped."

Seeded users with real JWT auth, no sign-up.
"The brief allows seeded accounts, so I skipped sign-up to keep the sharing demo
frictionless - but the auth is still real: hashed passwords, signed tokens,
enforced on the server."

Autosave instead of a save button.
"Edits save automatically with a 'saved' indicator, so it feels like Docs and you
can't lose work."

Tests target the risky logic, not easy wins.
"My 8 tests focus on the two things most likely to break silently - sharing
permissions and handling untrusted uploads - rather than padding coverage with
trivial assertions."

## AI usage (the honest version)
"I used an AI coding assistant to scaffold the boilerplate and draft tests, which
freed me to focus on the judgment calls - scope, the data model, the security
layer. I didn't trust any generated code until I ran it: in fact a test caught a
real bug where the email validator rejected my seeded domain, which I'd never have
spotted by eye. That's the point - AI for speed, me for judgment and verification."

## Closing line
"So the theme throughout is deliberate tradeoffs: a few things done well, each
choice made for a reason, and everything verified by actually running it."
