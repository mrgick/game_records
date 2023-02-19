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
