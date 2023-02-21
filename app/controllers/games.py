from typing import List

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..database.database import get_async_session, AsyncSession
from ..database.schemas import CreateGame, ReadGame, UpdateGame
from ..database.models import Game, Player
from ..config import settings

router = APIRouter(prefix="/games", tags=["games"])
views = Jinja2Templates(directory=settings.views_path)


@router.get("/", response_class=HTMLResponse, name='get_all_games')
async def get_all_games(
    request: Request, session: AsyncSession = Depends(get_async_session)
):
    games = await Game.get_all(session)
    print(games)
    return views.TemplateResponse(
        "games_table.html", {"request": request, "games": games}
    )


@router.get("/create", response_class=HTMLResponse, name="create_game_form")
async def create_game(
    request: Request, session: AsyncSession = Depends(get_async_session)
):
    players = await Player.get_all(session)
    return views.TemplateResponse(
        "create_game.html", {"request": request, "players": players}
    )


@router.post("/create", response_class=HTMLResponse, name="create_game")
async def create_game(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    game: CreateGame = Depends(CreateGame.as_form),
):
    _game = await Game.create(session, game)
    return views.TemplateResponse(
        "info.html", {"request": request, "message": f"Game created with id {_game.id}"}
    )


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
async def delete_game(game_id: int, session: AsyncSession = Depends(get_async_session)):
    await Game.delete(session, game_id)
    return {"status": True}
