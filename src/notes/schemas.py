from uuid import UUID

from pydantic import BaseModel


class NoteRead(BaseModel):
    id: int
    title: str
    body: str
    user_id: UUID


class NoteCreate(BaseModel):
    title: str
    body: str


class NoteUpdate(BaseModel):
    title: str | None = None
    body: str | None = None
