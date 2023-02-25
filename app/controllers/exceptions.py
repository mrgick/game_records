from starlette.requests import Request
from fastapi.templating import Jinja2Templates

from ..config import settings

views = Jinja2Templates(directory=settings.views_path)


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return views.TemplateResponse(
            "info.html", {"request": request, "error": f"Error: {str(e)}"}
        )
