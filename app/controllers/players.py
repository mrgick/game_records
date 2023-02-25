from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..database.database import get_async_session, AsyncSession
from ..database.schemas import CreatePlayer, UpdatePlayer
from ..database.models import Player
from ..config import settings

router = APIRouter(prefix="/players", tags=["players"])
views = Jinja2Templates(directory=settings.views_path)


@router.get("/", response_class=HTMLResponse, name="get_all_players")
async def get_all_players(
    request: Request, session: AsyncSession = Depends(get_async_session)
):
    players = await Player.get_all(session)
    return views.TemplateResponse(
        "players/players_table.html", {"request": request, "players": players}
    )


@router.get("/create", response_class=HTMLResponse, name="create_player_form")
async def create_player(request: Request):
    return views.TemplateResponse("players/player.html", {"request": request, "mode": "create"})


@router.post("/create", response_class=HTMLResponse, name="create_player")
async def create_player(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    player: CreatePlayer = Depends(CreatePlayer.as_form),
):
    _player = await Player.create(session, player)
    return views.TemplateResponse(
        "info.html",
        {
            "request": request,
            "message": f"Created player {_player.first_name} {_player.last_name} with id {_player.id}",
        },
    )


@router.get(
    "/update/{player_id}", response_class=HTMLResponse, name="update_player_form"
)
async def update_player(
    request: Request, player_id: int, session: AsyncSession = Depends(get_async_session)
):
    player = await Player.get(session, player_id)
    return views.TemplateResponse(
        "players/player.html", {"request": request, "mode": "update", "player": player}
    )


@router.post("/update/{player_id}", response_class=HTMLResponse, name="update_player")
async def update_player(
    request: Request,
    player_id: int,
    player: UpdatePlayer = Depends(UpdatePlayer.as_form),
    session: AsyncSession = Depends(get_async_session),
):
    _player = await Player.update(session, player_id, player)
    return views.TemplateResponse(
        "info.html",
        {
            "request": request,
            "message": f"Updated player {_player.first_name} {_player.last_name} with id {_player.id}",
        },
    )


@router.get("/{player_id}", response_class=HTMLResponse, name="get_player")
async def get_player(
    request: Request, player_id: int, session: AsyncSession = Depends(get_async_session)
):
    player = await Player.get(session, player_id)
    return views.TemplateResponse(
        "players/player.html", {"request": request, "mode": "read", "player": player}
    )
