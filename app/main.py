from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.leads import router as leads_router
from app.api.ui import router as ui_router
from app.core.config import settings
from app.middleware.demo_guard import DemoGuardMiddleware

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    root_path=settings.app_root_path,
)

if settings.demo_mode:
    app.add_middleware(DemoGuardMiddleware)

app.include_router(ui_router)
app.include_router(health_router)
app.include_router(leads_router, prefix="/api/v1")
