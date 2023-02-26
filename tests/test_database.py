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
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        return session


class TestPlayer:
    async def test_create_player(self, session):
        create_player = CreatePlayer(first_name="test", last_name="test")
        player = await Player.create(session, create_player)
        assert player == ReadPlayer(first_name="test", last_name="test", id=1)

    async def test_update_player(self, session):
        update_player = UpdatePlayer(first_name="test2", last_name="test2")
        player = await Player.update(session, 1, update_player)
        assert player == ReadPlayer(first_name="test2", last_name="test2", id=1)

    async def test_get_player(self, session):
        player = await Player.get(session, 1)
        assert player == ReadPlayer(first_name="test2", last_name="test2", id=1)

    async def test_get_all_players(self, session):
        players = await Player.get_all(session)
        assert players == [ReadPlayer(first_name="test2", last_name="test2", id=1)]
