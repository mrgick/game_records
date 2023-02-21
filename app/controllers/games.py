from typing import List

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..database.database import get_async_session, AsyncSession
from ..database.schemas import CreateGame, ReadGame, UpdateGame
from ..database.models import Game
from ..config import settings

router = APIRouter(prefix="/games", tags=["games"])
views = Jinja2Templates(directory=settings.views_path)


@router.get("/", response_model=List[ReadGame])
async def get_all_games(session: AsyncSession = Depends(get_async_session)):
    return await Game.get_all(session)


@router.post("/create", response_class=HTMLResponse)
async def create_game(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    game: CreateGame = Depends(CreateGame.as_form),
):
    await Game.create(session, game)
    return views.TemplateResponse("home.html", {"request": request})


@router.get("/{game_id}", response_model=ReadGame)
async def get_game(game_id: int, session: AsyncSession = Depends(get_async_session)):
    return await Game.get(session, game_id)


@router.put("/{game_id}", response_model=ReadGame)
async def update_game(
    game_id: int,
    game: UpdateGame = Depends(UpdateGame.as_form),
    session: AsyncSession = Depends(get_async_session),
):
    return await Game.update(session, game_id, game)


@router.delete("/{game_id}")
async def delete_game(
    game_id: int, session: AsyncSession = Depends(get_async_session)
):
    await Game.delete(session, game_id)
    return {"status": True}
