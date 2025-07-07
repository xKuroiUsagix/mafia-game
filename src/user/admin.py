from datetime import timedelta
from jwt import InvalidTokenError
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from src.db import get_db
from .utils import authenticate_user, create_access_token, get_token_data
from .constants import ADMIN_SESSION_TOKEN_EXPIRES_MINUTES
from .enums import RoleChoices


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request):
        form = await request.form()
        username, password = form['username'], form['password']

        async for db in get_db():
            user = await authenticate_user(db, username, password)

        if user is None or user.role != RoleChoices.ADMIN.value:
            return False
        
        access_token_expires = timedelta(minutes=ADMIN_SESSION_TOKEN_EXPIRES_MINUTES)
        access_token = create_access_token(
            data={
                'sub': user.username,
                'role': user.role
            },
            expires_delta=access_token_expires
        )
        request.session.update({'token': access_token})
        return True
    
    async def logout(self, request: Request):
        request.session.clear()
        return True
    
    async def authenticate(self, request: Request):
        token = request.session.get('token')
        if not token:
            return False
        
        try:
            payload = await get_token_data(token)
        except InvalidTokenError:
            return False
        
        role = payload.get('role')
        if role != RoleChoices.ADMIN.value:
            return False

        return True
