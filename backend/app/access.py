"""Centralized document access-control logic.

Keeping this in one place means every endpoint enforces the same rules, and the
rules are easy to read and test:

    owner  -> full control (edit content, rename, share, delete)
    edit   -> edit content + rename (collaborative)
    view   -> read only
    none   -> 404 (we hide existence of docs you can't see)
"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import Document, Share, User


def get_document_or_404(db: Session, doc_id: int) -> Document:
    doc = db.get(Document, doc_id)
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return doc


def role_for(db: Session, user: User, doc: Document) -> str | None:
    """Return the caller's role on a document, or None if no access."""
    if doc.owner_id == user.id:
        return "owner"
    share = (
        db.query(Share)
        .filter(Share.document_id == doc.id, Share.user_id == user.id)
        .one_or_none()
    )
    if share is None:
        return None
    return share.permission  # "edit" or "view"


def require_role(db: Session, user: User, doc: Document, need: str) -> str:
    """Ensure the caller meets a minimum role, else raise.

    need = "view" -> owner/edit/view all pass
    need = "edit" -> owner/edit pass
    need = "owner" -> only owner passes
    Absent access raises 404 (not 403) to avoid leaking document existence.
    """
    role = role_for(db, user, doc)
    if role is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

    ranking = {"view": 1, "edit": 2, "owner": 3}
    if ranking[role] < ranking[need]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"This action requires '{need}' access; you have '{role}'.",
        )
    return role
