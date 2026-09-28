import json
from hashlib import sha256

from sqlalchemy.orm import Session

from app.repositories.lead_repository import (
    create,
    get_by_fingerprint,
    update_automation_result,
)
from app.schemas.lead import (
    LeadAutomation,
    LeadCreate,
    LeadQualification,
    LeadResponse,
    LeadScoring,
)
from app.services.automation_service import dispatch_lead_automation
from app.services.followup_service import build_followup_draft
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


def _automation_from_existing(lead: object) -> LeadAutomation:
    return LeadAutomation(
        status=lead.automation_status,
        attempts=lead.automation_attempts,
        followup_draft=lead.followup_draft,
        last_error=lead.automation_last_error or None,
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
            automation=_automation_from_existing(existing),
        )

    qualification = qualify_lead(payload)
    scoring = score_lead(payload, qualification)
    followup_draft = build_followup_draft(payload, qualification, scoring)

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
        followup_draft=followup_draft,
    )

    automation_result = dispatch_lead_automation(
        lead_id=lead.id,
        payload=payload,
        qualification=qualification,
        scoring=scoring,
        followup_draft=followup_draft,
    )

    lead = update_automation_result(
        db,
        lead,
        status=automation_result.status,
        attempts=automation_result.attempts,
        last_error=automation_result.last_error,
    )

    return LeadResponse(
        id=lead.id,
        status=lead.status,
        duplicate=False,
        qualification=qualification.to_schema(),
        scoring=scoring.to_schema(),
        automation=_automation_from_existing(lead),
    )
