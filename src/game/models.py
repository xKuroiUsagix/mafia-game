from uuid import uuid4
from sqlalchemy import (
    String, ForeignKey, SmallInteger, CheckConstraint, UUID, UniqueConstraint, Enum
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models import TimestampModel, Base
from .enums import RoomType
from .constants import (
    DEFAULT_PLAYER_LIMIT,
    MIN_PLAYER_LIMIT,
    MIN_DAY_DURATION_MINUTES,
    MIN_NIGHT_DURATION_MINUTES
)


class Room(TimestampModel):
    __tablename__ = 'rooms'
    __table_args__ = (
        CheckConstraint(f'player_limit >= {MIN_PLAYER_LIMIT}', name='check_min_player_limit'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    creator: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    type_: Mapped[RoomType] = mapped_column(Enum(RoomType), nullable=False, default=RoomType.PUBLIC)
    rool_set_id: Mapped[int] = mapped_column(ForeignKey('rool_sets.id', ondelete='CASCADE'), nullable=False)
    join_code: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False, default=uuid4, unique=True)
    password: Mapped[str] = mapped_column(nullable=True)
    player_limit: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=DEFAULT_PLAYER_LIMIT)

    rool_set = relationship('RoolSet')
    creator = relationship('User', back_populates='rooms', uselist=False, cascade='all, delete')


class RoolSet(Base):
    __tablename__ = 'rool_sets'
    __table_args__ = (
        CheckConstraint(f'day_duration_minutes >= {MIN_DAY_DURATION_MINUTES}', name='check_min_day_duration'),
        CheckConstraint(f'night_duration_minutes >= {MIN_NIGHT_DURATION_MINUTES}', name='check_night_duration')
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    mafia_percent: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=25)
    allow_sherif: Mapped[bool] = mapped_column(nullable=False, default=True)
    day_duration_minutes: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=10)
    night_duration_minutes: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=5)

    game_roles = relationship('GameRole', secondary='rool_sets_roles', back_populates='rool_sets', cascade='all, delete')


class UserRoom(TimestampModel):
    __tablename__ = 'users_rooms'
    __table_args__ = (
        UniqueConstraint('user_id', 'room_id', name='unqiue_user_room'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id', ondelete='CASCADE'), nullable=False)
    is_creator: Mapped[bool] = mapped_column(nullable=False, default=False)


class GameRole(Base):
    __tablename__ = 'game_roles'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    is_mafia: Mapped[bool] = mapped_column(nullable=False, default=False)
    is_special: Mapped[bool] = mapped_column(nullable=False, default=False)

    rool_sets = relationship(
        'RoolSet', secondary='rool_sets_roles', back_populates='game_roles', cascade='all, delete'
    )


class RoolSetRole(Base):
    __tablename__ = 'rool_sets_roles'
    __table_args__ = (
        UniqueConstraint('rool_set_id', 'game_role_id', name='unique_rool_set_game_role'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    rool_set_id: Mapped[int] = mapped_column(ForeignKey('rool_sets.id', ondelete='CASCADE'), nullable=False)
    game_role_id: Mapped[int] = mapped_column(ForeignKey('game_roles.id', ondelete='CASCADE'), nullable=False)
