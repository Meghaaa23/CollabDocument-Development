"""Seed demo users and sample documents.

Runs idempotently on startup so a fresh clone / fresh deploy immediately has
accounts a reviewer can log in with and a pre-existing shared document to show
the "Shared with me" flow without any setup.
"""
from sqlalchemy.orm import Session

from .config import settings
from .models import Document, Share, User
from .sanitize import sanitize_html
from .security import hash_password

DEMO_USERS = [
    {"email": "alice@example.com", "name": "Alice Owner"},
    {"email": "bob@example.com", "name": "Bob Collaborator"},
    {"email": "carol@example.com", "name": "Carol Reviewer"},
]

_WELCOME_HTML = sanitize_html(
    "<h1>Welcome to CollabDocs</h1>"
    "<p>This is a seeded document owned by <strong>Alice</strong>. "
    "Try <strong>bold</strong>, <em>italic</em>, <u>underline</u>, headings and lists.</p>"
    "<h2>Things to try</h2>"
    "<ul><li>Rename this document (click the title)</li>"
    "<li>Share it from the <strong>Share</strong> button</li>"
    "<li>Upload a .txt, .md or .docx file to create a new doc</li></ul>"
)

_SHARED_HTML = sanitize_html(
    "<h1>Shared project notes</h1>"
    "<p>Alice shared this document with <strong>Bob</strong> (edit access). "
    "Log in as bob@example.com to see it under <em>Shared with me</em>.</p>"
    "<ol><li>Draft the outline</li><li>Review with the team</li><li>Ship it</li></ol>"
)


def seed(db: Session) -> None:
    created: dict[str, User] = {}
    for spec in DEMO_USERS:
        user = db.query(User).filter(User.email == spec["email"]).one_or_none()
        if user is None:
            user = User(
                email=spec["email"],
                name=spec["name"],
                password_hash=hash_password(settings.DEMO_PASSWORD),
            )
            db.add(user)
        created[spec["email"]] = user
    db.commit()

    alice = created["alice@example.com"]
    bob = created["bob@example.com"]

    # Only seed sample docs once (when Alice owns none).
    if db.query(Document).filter(Document.owner_id == alice.id).count() == 0:
        welcome = Document(title="Welcome to CollabDocs", content=_WELCOME_HTML, owner_id=alice.id)
        shared = Document(title="Shared project notes", content=_SHARED_HTML, owner_id=alice.id)
        db.add_all([welcome, shared])
        db.commit()
        db.refresh(shared)
        db.add(Share(document_id=shared.id, user_id=bob.id, permission="edit"))
        db.commit()
