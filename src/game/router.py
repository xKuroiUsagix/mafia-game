from fastapi import APIRouter, status, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession
from src.user import get_current_user, User
from src.db import get_db
from .service import room_service
from .schemas import (
    RoomResponse,
    RoomCreateRequest,
    RoomDetailResponse,
)


router = APIRouter(prefix='/rooms')


@router.post('', response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def create_room(
    room_data: RoomCreateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await room_service.create(room_data, db, current_user)


@router.post('/{join_code}')
async def join_room(
    join_code: str,
    password: str = Form(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await room_service.join_room(join_code, db, current_user, password)
    
    return { 'success': success }


@router.get('/{join_code}', response_model=RoomDetailResponse)
async def get_room(
    join_code: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await room_service.get_room(join_code, db, current_user)
