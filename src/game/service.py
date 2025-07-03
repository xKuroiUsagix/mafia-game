from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.user import User, get_password_hash, verify_password
from .models import Room, RoolSet, UserRoom
from .schemas import RoomCreateRequest, RoomResponse
from .enums import RoomType
from .constants import MAX_PLAYER_LIMIT


class RoomService:
    @staticmethod
    async def create(
        room_data: RoomCreateRequest,
        db: AsyncSession,
        user: User
    ) -> RoomResponse:
        if room_data.type_ == RoomType.PRIVATE and room_data.password is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='You should provide password for private room'
            )
        if room_data.player_limit > MAX_PLAYER_LIMIT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Current supported maximum number of players per room is {MAX_PLAYER_LIMIT}'
            )

        query = select(RoolSet).where(RoolSet.id == room_data.rool_set_id)
        result = await db.execute(query)
        rool_set = result.scalar_one_or_none()

        if not rool_set:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'RoolSet with id {room_data.rool_set_id} does not exist'
            )

        room = Room(
            type_=room_data.type_,
            rool_set_id=room_data.rool_set_id,
            join_code=uuid4(),
            password=get_password_hash(room_data.password),
            player_limit=room_data.player_limit
        )
        db.add(room)
        await db.commit()
        await db.refresh(room)

        return RoomResponse(
            id=room.id,
            type_=room.type_,
            rool_set_id=room.rool_set_id,
            join_code=room.join_code,
            player_limit=room.player_limit
        )


room_service = RoomService()
