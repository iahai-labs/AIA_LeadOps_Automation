from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.lead import Lead


def get_by_id(db: Session, lead_id: int) -> Lead | None:
    return db.get(Lead, lead_id)


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
    lead_score: int,
    lead_tier: str,
    recommended_action: str,
    score_reasons: str,
    followup_draft: str,
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
        lead_score=lead_score,
        lead_tier=lead_tier,
        recommended_action=recommended_action,
        score_reasons=score_reasons,
        followup_draft=followup_draft,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


def update_automation_result(
    db: Session,
    lead: Lead,
    *,
    status: str,
    attempts: int,
    last_error: str,
) -> Lead:
    lead.automation_status = status
    lead.automation_attempts = attempts
    lead.automation_last_error = last_error
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead
