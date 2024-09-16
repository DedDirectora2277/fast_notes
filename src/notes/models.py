import fastapi_users_db_sqlalchemy
from sqlalchemy import Column, Integer, String, Text, ForeignKey

from auth.models import User
from database import Base


class Note(Base):
    __tablename__ = "note"
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    body = Column(Text)
    user_id = Column(fastapi_users_db_sqlalchemy.generics.GUID(), ForeignKey(User.id), nullable=False)
