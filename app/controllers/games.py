from fastapi import APIRouter

router = APIRouter(prefix="/games", tags=['games'])


@router.get('')
async def get_all_games():
    return {"hello": "world!"}

