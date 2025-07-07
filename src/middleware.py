from jwt import InvalidTokenError
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from src.user.utils import get_token_data
from src.user.exceptions import CredentialsException


PUBLIC_ROUTES = (
    '/',
    '/token',
    '/users',
    '/docs',
    '/openapi.json',
    '/favicon.ico'
)


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if path in PUBLIC_ROUTES or path.startswith('/admin'):
            return await call_next(request)

        token = request.headers.get('Authorization')
        if not token:
            raise CredentialsException()

        if token.startswith('Bearer'):
            token = token[7:]

        try:
            payload = await get_token_data(token)
            username = payload.get('sub')

            if username is None:
                raise CredentialsException()
        except InvalidTokenError:
            raise CredentialsException()

        return await call_next(request)
