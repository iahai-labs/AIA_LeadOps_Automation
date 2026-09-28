from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.lead import Lead


def get_by_fingerprint(db: Session, fingerprint: str) -> Lead | None:
    return db.scalar(select(Lead).where(Lead.fingerprint == fingerprint))


def create(
    db: Session,
    *,
    name: str,
    email: str,
    company: str | None,
    message: str,
    fingerprint: str,
) -> Lead:
    lead = Lead(
        name=name,
        email=email,
        company=company,
        message=message,
        fingerprint=fingerprint,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead
