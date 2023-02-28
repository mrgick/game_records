from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..config import settings


router = APIRouter(tags=["base"])
templates = Jinja2Templates(directory=settings.templates_path)


@router.get("/", response_class=HTMLResponse, name="home")
async def index(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
