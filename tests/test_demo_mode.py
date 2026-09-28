from app.core.config import settings
from app.schemas.lead import LeadCreate
from app.services.automation_service import dispatch_lead_automation
from app.services.qualification_service import qualify_lead
from app.services.scoring_service import score_lead


def test_demo_mode_avoids_external_ai(monkeypatch) -> None:
    monkeypatch.setattr(settings, "demo_mode", True)
    monkeypatch.setattr(settings, "demo_disable_external_ai", True)

    payload = LeadCreate(
        name="Sarah Miller",
        email="sarah@example.com",
        company="Bright Dental",
        message="We need a website next month.",
    )

    result = qualify_lead(payload)

    assert result.source == "fallback"
    assert result.service_type == "website_development"


def test_demo_mode_skips_external_automation(monkeypatch) -> None:
    monkeypatch.setattr(settings, "demo_mode", True)
    monkeypatch.setattr(settings, "demo_disable_external_automation", True)

    payload = LeadCreate(
        name="Sarah Miller",
        email="sarah@example.com",
        company="Bright Dental",
        message="We need a website next month.",
    )
    qualification = qualify_lead(payload)
    scoring = score_lead(payload, qualification)

    result = dispatch_lead_automation(
        lead_id=1,
        payload=payload,
        qualification=qualification,
        scoring=scoring,
        followup_draft="Hi Sarah",
    )

    assert result.status == "skipped"
    assert result.attempts == 0
