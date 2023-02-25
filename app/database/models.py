from datetime import datetime

from sqlalchemy import ForeignKey, String, SmallInteger, exc
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    selectinload,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .schemas import (
    CreatePlayer,
    ReadPlayer,
    UpdatePlayer,
    CreateGame,
    ReadGame,
    UpdateGame,
)


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(64))

    @classmethod
    async def create(cls, session: AsyncSession, player: CreatePlayer) -> ReadPlayer:
        _player = Player(**player.dict())
        session.add(_player)
        await session.commit()
        return ReadPlayer.from_orm(_player)

    @classmethod
    async def update(
        cls, session: AsyncSession, id: int, player: UpdatePlayer
    ) -> ReadPlayer:
        statement = select(Player).where(Player.id == id)
        result = await session.execute(statement)
        _player = result.scalar_one()
        for attr, value in player.dict().items():
            if value:
                setattr(_player, attr, value)
        await session.commit()
        return ReadPlayer.from_orm(_player)

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> ReadPlayer:
        statement = select(Player).where(Player.id == id)
        result = await session.execute(statement)
        return ReadPlayer.from_orm(result.scalar_one())

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[ReadPlayer]:
        statement = select(Player)
        result = await session.execute(statement)
        return [ReadPlayer.from_orm(p) for p in result.scalars()]


class Game(Base):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime]
    player1_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    player2_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    player1: Mapped["Player"] = relationship(
        "Player", primaryjoin="Game.player1_id == Player.id"
    )
    player2: Mapped["Player"] = relationship(
        "Player", primaryjoin="Game.player2_id == Player.id"
    )
    status: Mapped[int] = mapped_column(SmallInteger(), default=0)

    @classmethod
    async def create(cls, session: AsyncSession, game: CreateGame) -> ReadGame:
        _game = Game(**game.dict())
        if _game.player1_id == _game.player2_id:
            raise exc.SQLAlchemyError("Players must be unique!")
        session.add(_game)
        await session.commit()
        return await cls.get(session, _game.id)

    @classmethod
    async def update(cls, session: AsyncSession, id: int, game: UpdateGame) -> ReadGame:
        statement = (
            select(Game)
            .where(Game.id == id)
            .options(selectinload(Game.player1), selectinload(Game.player2))
        )
        result = await session.execute(statement)
        _game = result.scalar_one()
        for attr, value in game.dict().items():
            if value:
                setattr(_game, attr, value)
        await session.commit()
        return ReadGame.from_orm(_game)

    @classmethod
    async def delete(cls, session: AsyncSession, id: int) -> None:
        statement = select(Game).where(Game.id == id)
        result = await session.execute(statement)
        await session.delete(result.scalar_one())
        await session.commit()

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> ReadGame:
        statement = (
            select(Game)
            .where(Game.id == id)
            .options(selectinload(Game.player1), selectinload(Game.player2))
        )
        result = await session.execute(statement)
        return ReadGame.from_orm(result.scalar_one())

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[ReadGame]:
        statement = select(Game).options(
            selectinload(Game.player1), selectinload(Game.player2)
        )
        result = await session.execute(statement)
        return [ReadGame.from_orm(g) for g in result.scalars()]
