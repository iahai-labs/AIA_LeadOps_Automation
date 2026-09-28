from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app

engine = create_engine(
    "sqlite+pysqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
Base.metadata.create_all(engine)


def override_get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_lead_detail_and_audit_endpoints() -> None:
    create_response = client.post(
        "/api/v1/leads",
        json={
            "name": "Sarah Miller",
            "email": "sarah@example.com",
            "company": "Bright Dental",
            "message": "We need a website next month.",
        },
    )
    assert create_response.status_code == 201
    lead_id = create_response.json()["id"]

    detail_response = client.get(f"/api/v1/leads/{lead_id}")
    assert detail_response.status_code == 200
    assert detail_response.json()["id"] == lead_id

    audit_response = client.get(f"/api/v1/leads/{lead_id}/audit")
    assert audit_response.status_code == 200
    assert audit_response.json()["lead_id"] == lead_id
    assert audit_response.json()["events"]
