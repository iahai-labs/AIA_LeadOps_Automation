from hashlib import sha256

from sqlalchemy.orm import Session

from app.repositories.lead_repository import create, get_by_fingerprint
from app.schemas.lead import LeadCreate, LeadQualification, LeadResponse
from app.services.qualification_service import qualify_lead


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


def create_lead(db: Session, payload: LeadCreate) -> LeadResponse:
    fingerprint = _fingerprint(payload)
    existing = get_by_fingerprint(db, fingerprint)

    if existing is not None:
        return LeadResponse(
            id=existing.id,
            status=existing.status,
            duplicate=True,
            qualification=_qualification_from_existing(existing),
        )

    qualification = qualify_lead(payload)

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
    )

    return LeadResponse(
        id=lead.id,
        status=lead.status,
        duplicate=False,
        qualification=qualification.to_schema(),
    )
