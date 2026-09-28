from app.core.config import settings
from app.integrations.n8n import WebhookResult, send_lead_webhook
from app.schemas.lead import LeadCreate
from app.services.qualification_service import QualificationResult
from app.services.scoring_service import ScoringResult


def build_automation_payload(
    *,
    lead_id: int,
    payload: LeadCreate,
    qualification: QualificationResult,
    scoring: ScoringResult,
    followup_draft: str,
) -> dict[str, object]:
    return {
        "event": "lead.created",
        "lead": {
            "id": lead_id,
            "name": payload.name,
            "email": str(payload.email),
            "company": payload.company,
            "message": payload.message,
        },
        "qualification": {
            "service_type": qualification.service_type,
            "intent": qualification.intent,
            "urgency": qualification.urgency,
            "summary": qualification.summary,
            "language": qualification.language,
            "source": qualification.source,
        },
        "scoring": {
            "score": scoring.score,
            "tier": scoring.tier,
            "recommended_action": scoring.recommended_action,
            "reasons": scoring.reasons,
        },
        "followup_draft": followup_draft,
        "notifications": {
            "telegram_recommended": scoring.tier == "hot",
        },
    }


def dispatch_lead_automation(
    *,
    lead_id: int,
    payload: LeadCreate,
    qualification: QualificationResult,
    scoring: ScoringResult,
    followup_draft: str,
) -> WebhookResult:
    if settings.demo_mode and settings.demo_disable_external_automation:
        return WebhookResult(status="skipped", attempts=0)

    webhook_payload = build_automation_payload(
        lead_id=lead_id,
        payload=payload,
        qualification=qualification,
        scoring=scoring,
        followup_draft=followup_draft,
    )
    return send_lead_webhook(webhook_payload)
