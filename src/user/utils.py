import jwt
from loguru import logger
from datetime import timedelta, datetime, timezone
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from src.config import settings
from src.db import get_db
from .models import User
from .exceptions import CredentialsException
from .schemas import TokenData


password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def verify_password(plain_password: str, hashed_password: str):
    return password_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_context.hash(password)


async def get_user(db: AsyncSession, username: str | None) -> User | None:
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def authenticate_user(db: AsyncSession, username: str, password: str) -> User | None:
    user = await get_user(db, username)
    if not user:
        return
    if not verify_password(password, user.password):
        return
    
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get('sub')

        if username is None:
            raise CredentialsException()
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise CredentialsException()
    
    user = await get_user(db, username=token_data.username)
    if user is None:
        logger.error(f'user {token_data.username} not found')
        raise CredentialsException()
    
    logger.info(f'request accepted from user {token_data.username}')
    return user
