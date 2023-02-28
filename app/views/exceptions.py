from starlette.requests import Request
from fastapi.templating import Jinja2Templates

from ..config import settings

templates = Jinja2Templates(directory=settings.templates_path)


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return templates.TemplateResponse(
            "info.html", {"request": request, "error": f"Error: {str(e)}"}
        )
