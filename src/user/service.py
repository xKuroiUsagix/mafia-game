from datetime import timedelta
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from src.config import settings
from .schemas import (
    UserCreateRequest,
    UserResponse,
    Token,
    ProfileCreateRequest,
    ProfileResponse,
)
from .models import User, Profile
from .utils import get_password_hash, authenticate_user, create_access_token
from .exceptions import CredentialsException


class UserService:

    @staticmethod
    async def create(user_data: UserCreateRequest, db: AsyncSession) -> UserResponse:
        query = select(User).where(
            or_(User.username == user_data.username, User.email == user_data.email)
        )
        result = await db.execute(query)
        user_exists = result.scalar_one_or_none()
        if user_exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='UserExists')

        try:
            user = User(
                username=user_data.username,
                email=user_data.email,
                password=get_password_hash(user_data.password)
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)

            return UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                role=user.role,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    @staticmethod
    async def login(form_data: OAuth2PasswordRequestForm, db: AsyncSession) -> Token:
        user = await authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise CredentialsException()
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                'sub': user.username,
                'role': user.role
            },
            expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type='bearer')
    
    @staticmethod
    async def create_profile(
        profile_data: ProfileCreateRequest, db: AsyncSession, user: User
    ) -> ProfileResponse:
        query = select(Profile).where(Profile.user_id == user.id)
        result = await db.execute(query)
        profile = result.scalar_one_or_none()

        if profile:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='ProfileExists')

        profile = Profile(
            user_id=user.id,
            description=profile_data.description
        )
        db.add(profile)
        await db.commit()
        await db.refresh(profile)

        return ProfileResponse(
            id=profile.id,
            user_id=profile.user_id,
            description=profile.description
        )
    
    @staticmethod
    async def get_profile(user: User, db: AsyncSession) -> ProfileResponse:
        query = select(Profile).where(Profile.user_id == user.id)
        result = await db.execute(query)
        profile = result.scalar_one_or_none()

        if not profile:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ProfileNotFound')

        return ProfileResponse(
            id=profile.id,
            user_id=profile.user_id,
            description=profile.description
        )


user_service = UserService()
