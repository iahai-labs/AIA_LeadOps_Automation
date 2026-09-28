from app.schemas.lead import LeadCreate
from app.services.automation_service import build_automation_payload
from app.services.qualification_service import QualificationResult
from app.services.scoring_service import ScoringResult


def test_automation_payload_marks_hot_lead_for_telegram() -> None:
    payload = LeadCreate(
        name="Sarah Miller",
        email="sarah@example.com",
        company="Bright Dental",
        message="We need a new website next month.",
    )
    qualification = QualificationResult(
        service_type="website_development",
        intent="high",
        urgency="high",
        summary="Dental clinic needs a website.",
        language="en",
        source="ai",
    )
    scoring = ScoringResult(
        score=90,
        tier="hot",
        recommended_action="Contact within 4 hours",
        reasons=["High intent"],
    )

    result = build_automation_payload(
        lead_id=42,
        payload=payload,
        qualification=qualification,
        scoring=scoring,
        followup_draft="Hi Sarah",
    )

    assert result["event"] == "lead.created"
    assert result["lead"]["id"] == 42
    assert result["scoring"]["tier"] == "hot"
    assert result["notifications"]["telegram_recommended"] is True
