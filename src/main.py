from fastapi import FastAPI
from sqladmin import Admin
from src.user.router import user_router, token_router
from src.user.admin import AdminAuth
from src.game.router import router as game_router
from src.game.admin import RoolSetAdminView, GameRoleAdminView
from src.middleware import AuthenticationMiddleware
from src.config import settings
from src.db import engine


app = FastAPI()

# When creating new public routes they should be added to PUBLIC_ROUTES in middleware.py
app.add_middleware(AuthenticationMiddleware)

admin_authentication = AdminAuth(settings.SECRET_KEY)
admin = Admin(app, engine=engine, authentication_backend=admin_authentication)

admin.add_view(RoolSetAdminView)
admin.add_view(GameRoleAdminView)

app.include_router(token_router, tags=['Auth'])
app.include_router(user_router, tags=['Users'])
app.include_router(game_router, tags=['Game'])
