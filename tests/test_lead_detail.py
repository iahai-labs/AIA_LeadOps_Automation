from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.db.base import Base
from app.schemas.lead import LeadCreate
from app.services.lead_service import create_lead, get_lead_detail


def test_get_lead_detail_returns_persisted_state() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    db = Session(engine)

    created = create_lead(
        db,
        LeadCreate(
            name="Sarah Miller",
            email="sarah@example.com",
            company="Bright Dental",
            message="We need a website next month.",
        ),
    )

    detail = get_lead_detail(db, created.id)

    assert detail is not None
    assert detail.id == created.id
    assert detail.email == "sarah@example.com"
    assert detail.scoring.score == created.scoring.score
    assert detail.automation.status == created.automation.status
