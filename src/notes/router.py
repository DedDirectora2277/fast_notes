from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, delete, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth import fastapi_users
from auth.models import User
from database import get_async_session
from notes.models import Note
from notes.schemas import NoteRead, NoteCreate, NoteUpdate
from starlette import status

router = APIRouter(
    prefix='/notes',
    tags=["Notes"]
)

current_user = fastapi_users.current_user()


@router.get('/', response_model=list[NoteRead])
async def get_notes_for_current_user(session: AsyncSession = Depends(get_async_session),
                                     user: User = Depends(current_user)):
    query = select(Note).where(Note.user_id == user.id)
    result = await session.execute(query)
    return result.scalars().all()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_note(note: NoteCreate, session: AsyncSession = Depends(get_async_session),
                   user: User = Depends(current_user)):
    stmt = insert(Note).values(**note.dict(), user_id=user.id).returning(Note)
    result = await session.execute(stmt)
    await session.commit()
    return result.scalars().first()


@router.delete('/{note_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    stmt = delete(Note).where(Note.id == note_id, Note.user_id == user.id)
    result = await session.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found or not accessible")
    await session.commit()
    return


@router.put('/{note_id}', response_model=NoteRead)
async def update_note(note_id: int, note_update: NoteUpdate, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    stmt = (
        update(Note)
        .where(Note.id == note_id, Note.user_id == user.id)
        .values(**note_update.dict(exclude_unset=True))
        .returning(Note)
    )
    result = await session.execute(stmt)
    updated_note = result.scalar_one_or_none()

    if updated_note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found or not accessible")

    await session.commit()
    return updated_note
