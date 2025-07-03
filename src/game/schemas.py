from uuid import UUID
from pydantic import BaseModel
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
