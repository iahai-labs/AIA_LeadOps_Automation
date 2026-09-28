from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.base import Base
from app.schemas.lead import LeadCreate
from app.services.lead_service import create_lead


def test_create_lead_and_detect_duplicate() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    db = Session(engine)

    payload = LeadCreate(
        name="Sarah Miller",
        email="sarah@example.com",
        company="Bright Dental",
        message="We need a new website and want to launch next month.",
    )

    first = create_lead(db, payload)
    second = create_lead(db, payload)

    assert first.duplicate is False
    assert second.duplicate is True
    assert first.id == second.id
