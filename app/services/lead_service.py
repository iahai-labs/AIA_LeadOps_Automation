import json
from hashlib import sha256

from sqlalchemy.orm import Session

from app.repositories.lead_repository import create, get_by_fingerprint
from app.schemas.lead import LeadCreate, LeadQualification, LeadResponse, LeadScoring
from app.services.qualification_service import qualify_lead
from app.services.scoring_service import score_lead


def _fingerprint(payload: LeadCreate) -> str:
    normalized = "|".join(
        [
            payload.email.strip().lower(),
            (payload.company or "").strip().lower(),
            payload.message.strip().lower(),
        ]
    )
    return sha256(normalized.encode("utf-8")).hexdigest()


def _qualification_from_existing(lead: object) -> LeadQualification:
    return LeadQualification(
        service_type=lead.service_type,
        intent=lead.intent,
        urgency=lead.urgency,
        summary=lead.qualification_summary,
        language=lead.language,
        source=lead.qualification_source,
    )


def _scoring_from_existing(lead: object) -> LeadScoring:
    try:
        reasons = json.loads(lead.score_reasons)
    except (TypeError, json.JSONDecodeError):
        reasons = []

    if not isinstance(reasons, list):
        reasons = []

    return LeadScoring(
        score=lead.lead_score,
        tier=lead.lead_tier,
        recommended_action=lead.recommended_action,
        reasons=[str(reason) for reason in reasons],
    )


def create_lead(db: Session, payload: LeadCreate) -> LeadResponse:
    fingerprint = _fingerprint(payload)
    existing = get_by_fingerprint(db, fingerprint)

    if existing is not None:
        return LeadResponse(
            id=existing.id,
            status=existing.status,
            duplicate=True,
            qualification=_qualification_from_existing(existing),
            scoring=_scoring_from_existing(existing),
        )

    qualification = qualify_lead(payload)
    scoring = score_lead(payload, qualification)

    lead = create(
        db,
        name=payload.name.strip(),
        email=str(payload.email).strip().lower(),
        company=payload.company.strip() if payload.company else None,
        message=payload.message.strip(),
        fingerprint=fingerprint,
        service_type=qualification.service_type,
        intent=qualification.intent,
        urgency=qualification.urgency,
        qualification_summary=qualification.summary,
        language=qualification.language,
        qualification_source=qualification.source,
        lead_score=scoring.score,
        lead_tier=scoring.tier,
        recommended_action=scoring.recommended_action,
        score_reasons=json.dumps(scoring.reasons),
    )

    return LeadResponse(
        id=lead.id,
        status=lead.status,
        duplicate=False,
        qualification=qualification.to_schema(),
        scoring=scoring.to_schema(),
    )
