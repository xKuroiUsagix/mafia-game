from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.user import get_current_user, User
from src.db import get_db
from .service import room_service
from .schemas import RoomResponse, RoomCreateRequest


router = APIRouter(prefix='/rooms')


@router.post('', response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def create_room(
    room_data: RoomCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await room_service.create(room_data, db, current_user)
