import enum
from datetime import datetime

from sqlalchemy import ForeignKey, String, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .schemas import CreatePlayer, ReadPlayer, UpdatePlayer


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
        _player = ReadPlayer.from_orm(_player)
        return _player

    @classmethod
    async def update(
        cls, session: AsyncSession, id: int, player: UpdatePlayer
    ) -> ReadPlayer:
        _player = Player(id=id, **player.dict())
        session.add(_player)
        await session.commit()
        return ReadPlayer.from_orm(_player)

    @classmethod
    async def delete(cls, session: AsyncSession, id: int) -> None:
        player = await session.get(id=id)
        await session.delete(player)

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> ReadPlayer:
        statement = select(Player).where(id=id)
        player = await session.execute(statement)
        return ReadPlayer.from_orm(player.one())

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list:
        statement = select(Player)
        players = await session.execute(statement)
        return [ReadPlayer.from_orm(p) for p in players.scalars()]


class Status(enum.Enum):
    not_started = 0
    winner_first = 1
    winner_second = 2
    draw = 3


class Game(Base):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime]
    player1_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    player2_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    player1 = relationship("Player", primaryjoin="Game.player1_id == Player.id")
    player2 = relationship("Player", primaryjoin="Game.player2_id == Player.id")
    status: Mapped["int"] = mapped_column(Enum(Status), default=Status.not_started)
