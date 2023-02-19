from typing import List

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..models.database import get_async_session, AsyncSession
from ..models.schemas import CreatePlayer, ReadPlayer, UpdatePlayer
from ..models.models import Player
from ..config import settings

router = APIRouter(prefix="/players", tags=["players"])
views = Jinja2Templates(directory=settings.views_path)


@router.get("/", response_model=List[ReadPlayer])
async def get_all_players(session: AsyncSession = Depends(get_async_session)):
    return await Player.get_all(session)


@router.get("/{player_id}", response_model=ReadPlayer)
async def get_player(
    player_id: int, session: AsyncSession = Depends(get_async_session)
):
    return await Player.get(session, player_id)


@router.put("/{player_id}", response_model=ReadPlayer)
async def update_player(
    player_id: int,
    player: UpdatePlayer,
    session: AsyncSession = Depends(get_async_session),
):
    return await Player.update(session, player_id, player)


@router.delete("/{player_id}")
async def delete_player(
    player_id: int, session: AsyncSession = Depends(get_async_session)
):
    await Player.delete(session, player_id)
    return {'status': True}


@router.get("/create", response_class=HTMLResponse, name="create_player_form")
async def create_player(request: Request):
    return views.TemplateResponse("create_player.html", {"request": request})


@router.post("/create", response_class=HTMLResponse, name="create_player")
async def create_player(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    player: CreatePlayer = Depends(CreatePlayer.as_form),
):
    await Player.create(session, player)
    return views.TemplateResponse("home.html", {"request": request})
