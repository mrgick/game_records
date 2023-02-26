import pytest

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.database.models import Base, Player, Game
from app.database.schemas import (
    CreatePlayer,
    UpdatePlayer,
    ReadPlayer,
    CreateGame,
    UpdateGame,
    ReadGame,
    GameStatus,
)


engine = create_async_engine(
    "sqlite+aiosqlite://",
    isolation_level="AUTOCOMMIT",
    connect_args={"check_same_thread": False},
)
async_session = async_sessionmaker(engine, expire_on_commit=False)

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

    async def test_create_player(self, session, player1_data):
        player = await Player.create(session, CreatePlayer(**player1_data))
        assert player == ReadPlayer(id=1, **player1_data)

    async def test_update_player(self, session, player, player2_data):
        _player = await Player.update(session, player.id, UpdatePlayer(**player2_data))
        assert _player == ReadPlayer(id=player.id, **player2_data)

    async def test_get_player(self, session, player, player1_data):
        await Player.create(session, CreatePlayer(**player1_data))
        _player = await Player.get(session, player.id)
        assert _player == ReadPlayer(id=player.id, **player1_data)

    async def test_get_all_players(self, session, player1_data, player2_data):
        player1 = await Player.create(session, CreatePlayer(**player1_data))
        player2 = await Player.create(session, CreatePlayer(**player2_data))
        players = await Player.get_all(session)
        assert players == [
            ReadPlayer(id=player1.id, **player1_data),
            ReadPlayer(id=player2.id, **player2_data),
        ]


class TestGame:
    @pytest.fixture
    @classmethod
    async def players(cls, session, player1_data, player2_data):
        await Player.create(session, CreatePlayer(**player1_data))
        await Player.create(session, CreatePlayer(**player2_data))
        players = await Player.get_all(session)
        return players

    @pytest.fixture
    @classmethod
    async def game(cls, session, game_data):
        game = await Game.create(session, CreateGame(**game_data))
        return game

    async def test_create_game(self, session, players, game_data):
        game = await Game.create(session, CreateGame(**game_data))
        assert game == ReadGame(
            id=1, player1=players[0], player2=players[1], **game_data
        )

    async def test_update_game(self, session, players, game_data):
        await Game.create(session, CreateGame(**game_data))
        game = await Game.update(session, 1, UpdateGame(status=GameStatus.winner_first))
        assert game == ReadGame(
            id=1,
            player1=players[0],
            player2=players[1],
            **{**game_data, "status": GameStatus.winner_first}
        )

    async def test_get_game(self, session, players, game_data):
        await Game.create(session, CreateGame(**game_data))
        game = await Game.get(session, 1)
        assert game == ReadGame(
            id=1,
            player1=players[0],
            player2=players[1],
            **{**game_data, "status": GameStatus.not_started}
        )

    async def test_get_all_games(self, session, players, game_data):
        await Game.create(session, CreateGame(**game_data))
        games = await Game.get_all(session)
        assert games == [
            ReadGame(
                id=1,
                player1=players[0],
                player2=players[1],
                **{**game_data, "status": GameStatus.not_started}
            )
        ]
