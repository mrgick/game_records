import pytest
from httpx import AsyncClient

from .db import engine, async_session

from app.main import app
from app.database.database import get_async_session
from app.database.models import Base, Player, Game
from app.database.schemas import (
    CreatePlayer,
    ReadPlayer,
    CreateGame,
    ReadGame,
    GameStatus,
)

pytestmark = pytest.mark.anyio


@pytest.fixture(
    params=[
        pytest.param(("asyncio", {"use_uvloop": False}), id="asyncio"),
    ]
)
def anyio_backend(request):
    return request.param


@pytest.fixture
async def session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        yield session


async def async_test_session():
    async with async_session() as session:
        yield session


app.dependency_overrides[get_async_session] = async_test_session


class TestHome:
    async def test_home(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/")
        assert response.status_code == 200


@pytest.fixture
def player1_data():
    return {"first_name": "test", "last_name": "test"}


@pytest.fixture
def player2_data():
    return {"first_name": "test2", "last_name": "test2"}


@pytest.fixture
def game_data():
    return {
        "date": "2023-03-27 11:30:00",
        "player1_id": 1,
        "player2_id": 2,
        "status": GameStatus.not_started,
    }


class TestPlayer:
    @pytest.fixture
    @classmethod
    async def player(cls, session, player1_data):
        player = await Player.create(session, CreatePlayer(**player1_data))
        return player

    async def test_create_player_form(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/players/create")
        assert response.status_code == 200

    async def test_create_player(self, session, player1_data):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/players/create", data=player1_data)
        assert response.status_code == 200
        player = await Player.get(session, 1)
        assert player == ReadPlayer(id=1, **player1_data)

    async def test_update_player_form(self, player):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f"/players/update/{player.id}")
        assert response.status_code == 200

    async def test_update_player(self, session, player, player2_data):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(f"/players/update/{player.id}", data=player2_data)
        assert response.status_code == 200
        _player = await Player.get(session, player.id)
        assert _player == ReadPlayer(id=player.id, **player2_data)

    async def test_get_player(self, player):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f"/players/{player.id}")
        assert response.status_code == 200

    async def test_get_all_players(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/players/")
        assert response.status_code == 200


class TestGame:
    @pytest.fixture
    @classmethod
    async def players(cls, session, player1_data, player2_data):
        player1 = await Player.create(session, CreatePlayer(**player1_data))
        player2 = await Player.create(session, CreatePlayer(**player2_data))
        return [player1, player2]

    @pytest.fixture
    @classmethod
    async def game(cls, session, players, game_data):
        game = await Game.create(session, CreateGame(**game_data))
        return game

    async def test_create_game_form(self):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/games/create")
        assert response.status_code == 200

    async def test_create_game(self, session, players, game_data):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post("/games/create", data=game_data)
        assert response.status_code == 200
        game = await Game.get(session, 1)
        assert game == ReadGame(
            id=1, player1=players[0], player2=players[1], **game_data
        )

    async def test_update_game_form(self, game):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f"/games/update/{game.id}")
        assert response.status_code == 200

    async def test_update_game(self, session, game):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                f"/games/update/{game.id}", data={"status": GameStatus.draw}
            )
        assert response.status_code == 200
        _game = await Game.get(session, game.id)
        assert _game == ReadGame(
            **{**game.dict(), "status": GameStatus.draw},
        )

    async def test_delete_game(self, session, game):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(f"/games/delete/{game.id}")
        assert response.status_code == 200
        games = await Game.get_all(session)
        assert games == []

    async def test_get_game(self, game):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get(f"/games/{game.id}")
        assert response.status_code == 200

    async def test_get_all_games(self, game):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/games/")
        assert response.status_code == 200
