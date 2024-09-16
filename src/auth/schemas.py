import uuid
from datetime import datetime
from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str
    registered_at: Optional[datetime] = None


class UserCreate(schemas.BaseUserCreate):
    username: str


class UserUpdate(schemas.BaseUserUpdate):
    username: str
    registered_at: Optional[datetime] = None

