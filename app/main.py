from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .controllers import games, home, players
from .config import settings


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
)

app.mount("/static", StaticFiles(directory=settings.static_path), name="static")

app.include_router(home.router)
app.include_router(games.router)
app.include_router(players.router)
