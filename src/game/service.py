from uuid import uuid4
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from src.user import User, get_password_hash, verify_password
from .models import Room, RoolSet, UserRoom
from .schemas import (
    RoomCreateRequest,
    RoomResponse,
    RoomDetailResponse,
    GameRoleResponse,
    RoolSetResponse,
    UserInRoom,
)
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
            creator_id=user.id,
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
            player_limit=room.player_limit,
            created_at=room.created_at,
            updated_at=room.updated_at
        )

    @staticmethod
    async def join_room(
        join_code: str,
        db: AsyncSession,
        user: User,
        password: str = None
    ) -> bool:
        query = (
            select(Room)
            .options(selectinload(Room.users))
            .where(Room.join_code == join_code)
        )
        result = await db.execute(query)
        room = result.scalar_one_or_none()

        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Room does not exist'
            )
        
        existing_membership = await db.execute(
            select(UserRoom)
            .where(
                UserRoom.user_id == user.id,
                UserRoom.room_id == room.id
            )
        )
        if existing_membership.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='You have already joined this room'
            )

        if room.creator_id == user.id:
            user_room = UserRoom(
                user_id=user.id,
                room_id=room.id,
                is_creator=True
            )
            db.add(user_room)
            await db.commit()
            return True

        if room.type_ == RoomType.PRIVATE.value and password is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='This room requires password to join'
            )
        if room.type_ == RoomType.PRIVATE.value and not verify_password(password, room.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Password incorrect'
            )
        
        query = select(func.count()).select_from(UserRoom).where(UserRoom.room_id == room.id)
        result = await db.execute(query)
        user_count = result.scalar_one()

        if user_count >= room.player_limit:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Room is full'
            )
        
        user_room = UserRoom(
            user_id=user.id,
            room_id=room.id,
            is_creator=False
        )
        db.add(user_room)
        await db.commit()
        return True
    
    @staticmethod
    async def get_room(
        join_code: str, 
        db: AsyncSession, 
        user: User
    ):
        query = (
            select(Room)
            .options(
                selectinload(Room.rool_set).selectinload(RoolSet.game_roles),
                selectinload(Room.users)
            )
            .where(Room.join_code == join_code)
        )
        result = await db.execute(query)
        room = result.scalar_one_or_none()

        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Room does not exist'
            )
        if user not in room.users and room.creator != user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='You cannot recieve information about this room'
            )
        
        query = select(func.count()).select_from(UserRoom).where(UserRoom.room_id == room.id)
        result = await db.execute(query)
        player_count = result.scalar_one()

        game_roles = [
            GameRoleResponse(
                id=gr.id,
                name=gr.name,
                is_mafia=gr.is_mafia,
                is_special=gr.is_special
            )
            for gr in room.rool_set.game_roles
        ]

        rool_set = RoolSetResponse(
            id=room.rool_set_id,
            name=room.rool_set.name,
            mafia_percent=room.rool_set.mafia_percent,
            allow_sheriff=room.rool_set.allow_sheriff,
            day_duration_minutes=room.rool_set.day_duration_minutes,
            night_duration_minutes=room.rool_set.night_duration_minutes,
            game_roles=game_roles
        )

        players = [
            UserInRoom.model_validate(u)
            for u in room.users
        ]
        
        return RoomDetailResponse(
            id=room.id,
            type_=room.type_,
            join_code=join_code,
            player_limit=room.player_limit,
            rool_set=rool_set,
            player_count=player_count,
            players=players,
            created_at=room.created_at,
            updated_at=room.updated_at
        )


room_service = RoomService()
