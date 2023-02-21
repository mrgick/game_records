from enum import IntEnum
from datetime import datetime

from pydantic import BaseModel, Field

from .schemas_as_form import as_form


class BasePlayer(BaseModel):
    first_name: str = Field(max_length=64)
    last_name: str = Field(max_length=64)


@as_form
class CreatePlayer(BasePlayer):
    pass


@as_form
class UpdatePlayer(BasePlayer):
    first_name: str | None = Field(max_length=64)
    last_name: str | None = Field(max_length=64)

    class Config:
        orm_mode = True


class ReadPlayer(BasePlayer):
    id: int

    class Config:
        orm_mode = True


class GameStatus(IntEnum):
    not_started = 0
    winner_first = 1
    winner_second = 2
    draw = 3


class BaseGame(BaseModel):
    date: datetime
    player1_id: int
    player2_id: int
    status: GameStatus = GameStatus.not_started


@as_form
class CreateGame(BaseGame):
    pass


@as_form
class UpdateGame(BaseGame):
    date: datetime | None
    player1_id: int | None
    player2_id: int | None
    status: GameStatus | None

    class Config:
        orm_mode = True


class ReadGame(BaseGame):
    id: int
    player1: ReadPlayer
    player2: ReadPlayer

    class Config:
        orm_mode = True
