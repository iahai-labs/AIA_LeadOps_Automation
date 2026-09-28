from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.base import Base
from app.repositories.audit_repository import list_events_for_lead
from app.schemas.lead import LeadCreate
from app.services.lead_service import create_lead


def test_lead_creation_records_audit_events() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    db = Session(engine)

    payload = LeadCreate(
        name="Sarah Miller",
        email="sarah@example.com",
        company="Bright Dental",
        message="We need a website next month.",
    )

    result = create_lead(db, payload)
    events = list_events_for_lead(db, result.id)
    event_types = [event.event_type for event in events]

    assert "lead.created" in event_types
    assert "automation.skipped" in event_types
