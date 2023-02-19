import enum
from datetime import datetime

from sqlalchemy import ForeignKey, String, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(64))
    last_name: Mapped[str] = mapped_column(String(64))


class Status(enum.Enum):
    not_started = 0
    winner_first = 1
    winner_second = 2
    draw = 3


class Game(Base):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime]
    first_player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    first_player: Mapped["Player"] = relationship(back_populates="players")
    second_player_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    second_player: Mapped["Player"] = relationship(back_populates="players")
    status: Mapped["int"] = mapped_column(Enum(Status), default=Status.not_started)
