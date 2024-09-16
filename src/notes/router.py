from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import fastapi_users
from auth.models import User
from database import get_async_session
from notes.models import Note
from notes.schemas import NoteRead, NoteCreate

router = APIRouter(
    prefix='/notes',
    tags=["Notes"]
)


current_user = fastapi_users.current_user()


@router.get('/')
async def get_notes_for_current_user(session: AsyncSession = Depends(get_async_session),
                                     user: User = Depends(current_user)):
    query = select(Note).where(Note.user_id == user.id)
    result = await session.execute(query)
    return result.mappings().all()


@router.post('/')
async def add_note(note: NoteCreate, session: AsyncSession = Depends(get_async_session),
                   user: User = Depends(current_user)):
    stmt = insert(Note).values(**note.dict(), user_id=user.id)
    await session.execute(stmt)
    await session.commit()
    return {'status': 'success'}


@router.delete('/{note_id}')
async def delete_note(note_id: int, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    stmt = delete(Note).where(Note.id == note_id and Note.user_id == user.id)
    await session.execute(stmt)
    await session.commit()
    return {'status': 'success'}

