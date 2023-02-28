from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .views import games, home, players
from .views.exceptions import catch_exceptions_middleware
from .config import settings


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
)

app.middleware('http')(catch_exceptions_middleware)

app.mount("/static", StaticFiles(directory=settings.static_path), name="static")

app.include_router(home.router)
app.include_router(games.router)
app.include_router(players.router)

@app.on_event("startup")
async def startup_event():
    from .database.database import init_db
    await init_db()
