from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import Document, Share, User


def get_document_or_404(db: Session, doc_id: int) -> Document:
    doc = db.get(Document, doc_id)
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    return doc


def role_for(db: Session, user: User, doc: Document) -> str | None:
    if doc.owner_id == user.id:
        return "owner"
    share = (
        db.query(Share)
        .filter(Share.document_id == doc.id, Share.user_id == user.id)
        .one_or_none()
    )
    if share is None:
        return None
    return share.permission


def require_role(db: Session, user: User, doc: Document, need: str) -> str:
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
