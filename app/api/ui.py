from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(include_in_schema=False)
WEB_ROOT = Path(__file__).resolve().parent.parent / "web"


@router.get("/")
def demo_ui() -> FileResponse:
    return FileResponse(WEB_ROOT / "index.html")
