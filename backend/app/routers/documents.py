from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from ..access import get_document_or_404, require_role
from ..config import settings
from ..database import get_db
from ..file_import import UnsupportedFileType, import_file
from ..models import Document, Share, User
from ..sanitize import sanitize_html
from ..schemas import (
    DocumentCreate,
    DocumentDetail,
    DocumentSummary,
    DocumentUpdate,
    ShareCreate,
    ShareOut,
)
from ..security import get_current_user

router = APIRouter(prefix="/api/documents", tags=["documents"])


def _summary(doc: Document, role: str) -> dict:
    return {
        "id": doc.id,
        "title": doc.title,
        "owner": doc.owner,
        "updated_at": doc.updated_at,
        "is_owner": role == "owner",
        "role": role,
    }


def _detail(db: Session, doc: Document, role: str) -> dict:
    data = _summary(doc, role)
    data["content"] = doc.content
    data["shares"] = [ShareOut.model_validate(s) for s in doc.shares] if role == "owner" else []
    return data


@router.get("", response_model=list[DocumentSummary])
def list_documents(
    db: Session = Depends(get_db), current: User = Depends(get_current_user)
):
    owned = db.query(Document).filter(Document.owner_id == current.id).all()
    shared_rows = (
        db.query(Document, Share.permission)
        .join(Share, Share.document_id == Document.id)
        .filter(Share.user_id == current.id)
        .all()
    )

    items = [_summary(doc, "owner") for doc in owned]
    items += [_summary(doc, perm) for doc, perm in shared_rows]
    items.sort(key=lambda d: d["updated_at"], reverse=True)
    return items


@router.post("", response_model=DocumentDetail, status_code=status.HTTP_201_CREATED)
def create_document(
    body: DocumentCreate,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    doc = Document(
        title=body.title.strip() or "Untitled document",
        content=sanitize_html(body.content),
        owner_id=current.id,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return _detail(db, doc, "owner")


@router.post("/upload", response_model=DocumentDetail, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    raw = await file.read()
    if len(raw) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File is empty")
    if len(raw) > settings.MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds {settings.MAX_UPLOAD_BYTES // (1024 * 1024)} MB limit",
        )
    try:
        title, html = import_file(file.filename or "upload", raw)
    except UnsupportedFileType as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Could not read that file. It may be corrupt or malformed.",
        )

    doc = Document(title=title, content=sanitize_html(html), owner_id=current.id)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return _detail(db, doc, "owner")


@router.get("/{doc_id}", response_model=DocumentDetail)
def get_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    doc = get_document_or_404(db, doc_id)
    role = require_role(db, current, doc, need="view")
    return _detail(db, doc, role)


@router.patch("/{doc_id}", response_model=DocumentDetail)
def update_document(
    doc_id: int,
    body: DocumentUpdate,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    doc = get_document_or_404(db, doc_id)
    role = require_role(db, current, doc, need="edit")
    if body.title is not None:
        doc.title = body.title.strip() or "Untitled document"
    if body.content is not None:
        doc.content = sanitize_html(body.content)
    db.commit()
    db.refresh(doc)
    return _detail(db, doc, role)


@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    doc_id: int,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    doc = get_document_or_404(db, doc_id)
    require_role(db, current, doc, need="owner")
    db.delete(doc)
    db.commit()


@router.get("/{doc_id}/shares", response_model=list[ShareOut])
def list_shares(
    doc_id: int,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    doc = get_document_or_404(db, doc_id)
    require_role(db, current, doc, need="owner")
    return [ShareOut.model_validate(s) for s in doc.shares]


@router.post("/{doc_id}/shares", response_model=ShareOut, status_code=status.HTTP_201_CREATED)
def add_share(
    doc_id: int,
    body: ShareCreate,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    doc = get_document_or_404(db, doc_id)
    require_role(db, current, doc, need="owner")

    target = db.query(User).filter(User.email == body.email.lower()).one_or_none()
    if target is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user with email {body.email}. Try a seeded demo account.",
        )
    if target.id == current.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="You already own this document"
        )

    existing = (
        db.query(Share)
        .filter(Share.document_id == doc.id, Share.user_id == target.id)
        .one_or_none()
    )
    if existing:
        existing.permission = body.permission
        share = existing
    else:
        share = Share(document_id=doc.id, user_id=target.id, permission=body.permission)
        db.add(share)
    db.commit()
    db.refresh(share)
    return ShareOut.model_validate(share)


@router.delete("/{doc_id}/shares/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_share(
    doc_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current: User = Depends(get_current_user),
):
    doc = get_document_or_404(db, doc_id)
    require_role(db, current, doc, need="owner")
    share = (
        db.query(Share)
        .filter(Share.document_id == doc.id, Share.user_id == user_id)
        .one_or_none()
    )
    if share is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Share not found")
    db.delete(share)
    db.commit()
