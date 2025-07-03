from fastapi import FastAPI
from src.user.router import user_router, token_router
from src.game.router import router as game_router


app = FastAPI()

app.include_router(token_router, tags=['Auth'])
app.include_router(user_router, tags=['Users'])
app.include_router(game_router, tags=['Game'])
