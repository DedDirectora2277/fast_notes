from fastapi import FastAPI

from auth.auth import fastapi_users, auth_backend
from auth.schemas import UserRead, UserCreate, UserUpdate
from notes.router import router as notes_router

app = FastAPI(
    title='MyNotes'
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(notes_router)

