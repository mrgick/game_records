from fastapi import APIRouter


router = APIRouter(tags=['base'])


@router.get('/')
async def index():
    return {"hello": "world!"}

