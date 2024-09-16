from pydantic import BaseModel


class NoteRead(BaseModel):
    id: int
    title: str
    body: str
    user_id: str


class NoteCreate(BaseModel):
    title: str
    body: str


