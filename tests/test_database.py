import functools
import anyio
import pytest


from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.database.models import Base, Player, Game
from app.database.schemas import CreatePlayer, UpdatePlayer, ReadPlayer


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


class TestPlayer:
    async def test_create_player(self, session, player1_data):
        player = await Player.create(session, CreatePlayer(**player1_data))
        assert player == ReadPlayer(id=1, **player1_data)

    async def test_update_player(self, session, player1_data, player2_data):
        await Player.create(session, CreatePlayer(**player1_data))
        player = await Player.update(session, 1, UpdatePlayer(**player2_data))
        assert player == ReadPlayer(id=1, **player2_data)

    async def test_get_player(self, session, player1_data):
        await Player.create(session, CreatePlayer(**player1_data))
        player = await Player.get(session, 1)
        assert player == ReadPlayer(id=1, **player1_data)

    async def test_get_all_players(self, session, player1_data, player2_data):
        await Player.create(session, CreatePlayer(**player1_data))
        await Player.create(session, CreatePlayer(**player2_data))
        players = await Player.get_all(session)
        assert players == [
            ReadPlayer(id=1, **player1_data),
            ReadPlayer(id=2, **player2_data),
        ]
