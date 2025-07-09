from datetime import datetime
from uuid import UUID
from typing import List
from pydantic import BaseModel
from src.user.schemas import UserInRoom
from .enums import RoomType
from .constants import DEFAULT_PLAYER_LIMIT


class RoomCreateRequest(BaseModel):
    type_: RoomType = RoomType.PUBLIC
    rool_set_id: int
    password: str | None = None
    player_limit: int = DEFAULT_PLAYER_LIMIT


class RoomResponse(BaseModel):
    id: int
    type_: RoomType
    rool_set_id: int
    join_code: UUID
    player_limit: int
    created_at: datetime
    updated_at: datetime


class GameRoleResponse(BaseModel):
    id: int
    name: str
    is_mafia: bool
    is_special: bool


class RoolSetResponse(BaseModel):
    id: int
    name: str
    mafia_percent: int
    allow_sheriff: bool
    day_duration_minutes: int
    night_duration_minutes: int
    game_roles: List[GameRoleResponse]


class RoomDetailResponse(BaseModel):
    id: int
    type_: RoomType
    join_code: UUID
    player_limit: int
    rool_set: RoolSetResponse
    player_count: int = 0
    players: List[UserInRoom] = []
    created_at: datetime
    updated_at: datetime
