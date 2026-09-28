from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.core.config import settings
from app.middleware.demo_guard import DemoGuardMiddleware


def test_demo_guard_rate_limits_post_requests(monkeypatch) -> None:
    monkeypatch.setattr(settings, "demo_rate_limit_per_minute", 1)

    app = FastAPI()
    app.add_middleware(DemoGuardMiddleware)

    @app.post("/api/v1/leads")
    def create_lead() -> dict[str, bool]:
        return {"ok": True}

    client = TestClient(app)

    first = client.post("/api/v1/leads", headers={"X-Real-IP": "203.0.113.10"})
    second = client.post("/api/v1/leads", headers={"X-Real-IP": "203.0.113.10"})

    assert first.status_code == 200
    assert second.status_code == 429
