from app.schemas.lead import LeadCreate
from app.services.followup_service import build_followup_draft
from app.services.qualification_service import QualificationResult
from app.services.scoring_service import ScoringResult


def test_hot_lead_followup_is_action_oriented() -> None:
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
        reasons=[],
    )

    draft = build_followup_draft(payload, qualification, scoring)

    assert draft.startswith("Hi Sarah")
    assert "website development project" in draft
    assert "as soon as possible" in draft
