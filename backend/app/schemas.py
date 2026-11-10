"""Pydantic request/response schemas (the API contract + input validation)."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ---- Auth ----
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=200)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    name: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---- Documents ----
class DocumentCreate(BaseModel):
    title: str = Field(default="Untitled document", min_length=1, max_length=255)
    content: str = Field(default="")


class DocumentUpdate(BaseModel):
    """Partial update: rename, edit content, or both."""
    title: str | None = Field(default=None, min_length=1, max_length=255)
    content: str | None = None


class ShareOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    permission: str
    user: UserOut


class DocumentSummary(BaseModel):
    """Lightweight shape used in list views (no content body)."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    owner: UserOut
    updated_at: datetime
    # Set by the API per-request: is the caller the owner of this doc?
    is_owner: bool
    role: str  # "owner" | "edit" | "view"


class DocumentDetail(DocumentSummary):
    content: str
    shares: list[ShareOut] = []


# ---- Sharing ----
class ShareCreate(BaseModel):
    email: EmailStr
    permission: str = Field(default="edit", pattern="^(edit|view)$")
