from fastapi import FastAPI

from .controllers import base, games, players
from .config import settings


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
)

app.include_router(base.router)
app.include_router(games.router)
app.include_router(players.router)



