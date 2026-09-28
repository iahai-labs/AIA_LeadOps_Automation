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
    service_type: str,
    intent: str,
    urgency: str,
    qualification_summary: str,
    language: str,
    qualification_source: str,
) -> Lead:
    lead = Lead(
        name=name,
        email=email,
        company=company,
        message=message,
        fingerprint=fingerprint,
        service_type=service_type,
        intent=intent,
        urgency=urgency,
        qualification_summary=qualification_summary,
        language=language,
        qualification_source=qualification_source,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead
