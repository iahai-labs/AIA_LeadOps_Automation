from hashlib import sha256

from sqlalchemy.orm import Session

from app.repositories.lead_repository import create, get_by_fingerprint
from app.schemas.lead import LeadCreate, LeadResponse


def _fingerprint(payload: LeadCreate) -> str:
    normalized = "|".join(
        [
            payload.email.strip().lower(),
            (payload.company or "").strip().lower(),
            payload.message.strip().lower(),
        ]
    )
    return sha256(normalized.encode("utf-8")).hexdigest()


def create_lead(db: Session, payload: LeadCreate) -> LeadResponse:
    fingerprint = _fingerprint(payload)
    existing = get_by_fingerprint(db, fingerprint)

    if existing is not None:
        return LeadResponse(
            id=existing.id,
            status=existing.status,
            duplicate=True,
        )

    lead = create(
        db,
        name=payload.name.strip(),
        email=str(payload.email).strip().lower(),
        company=payload.company.strip() if payload.company else None,
        message=payload.message.strip(),
        fingerprint=fingerprint,
    )

    return LeadResponse(
        id=lead.id,
        status=lead.status,
        duplicate=False,
    )
