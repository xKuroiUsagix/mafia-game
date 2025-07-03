from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from src.db import get_db
from .schemas import (
    UserCreateRequest,
    UserResponse,
    Token,
    ProfileCreateRequest,
)
from .service import user_service
from .utils import get_current_user
from .models import User


user_router = APIRouter(prefix='/users')
token_router = APIRouter(prefix='/token')


@token_router.post('')
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
) -> Token:
    return await user_service.login(form_data, db)


@user_router.post('', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    return await user_service.create(user_data, db)


@user_router.post('/profile')
async def create_profile(
    profile_data: ProfileCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await user_service.create_profile(profile_data, db, current_user)


@user_router.get('/profile')
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await user_service.get_profile(current_user, db)
