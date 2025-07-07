from typing import Optional
from sqlalchemy import (
    String, ForeignKey, Text
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models import TimestampModel, Base
from .enums import RoleChoices


class User(TimestampModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(256), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    role: Mapped[str] = mapped_column(String(32), nullable=False, default=RoleChoices.USER.value)

    profile = relationship(
        'Profile', back_populates='user', uselist=False, cascade='all, delete'
    )
    rooms = relationship('Room', back_populates='creator', cascade='all, delete')


class Profile(Base):
    __tablename__ = 'profiles'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    user = relationship('User', back_populates='profile', uselist=False)
