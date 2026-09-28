from app.schemas.lead import LeadCreate
from app.services.qualification_service import QualificationResult
from app.services.scoring_service import score_lead


def test_high_intent_urgent_lead_scores_hot() -> None:
    payload = LeadCreate(
        name="Sarah Miller",
        email="sarah@example.com",
        company="Bright Dental",
        message=(
            "We need a new website for our dental clinic and want to launch next month. "
            "Please send us a proposal."
        ),
    )
    qualification = QualificationResult(
        service_type="website_development",
        intent="high",
        urgency="high",
        summary="Dental clinic needs a website next month.",
        language="en",
        source="ai",
    )

    result = score_lead(payload, qualification)

    assert result.score == 100
    assert result.tier == "hot"
    assert result.recommended_action == "Contact within 4 hours"
    assert result.reasons


def test_low_signal_lead_scores_cold() -> None:
    payload = LeadCreate(
        name="Alex Smith",
        email="alex@example.com",
        company=None,
        message="Just checking prices.",
    )
    qualification = QualificationResult(
        service_type="unknown",
        intent="low",
        urgency="unknown",
        summary="Price inquiry.",
        language="en",
        source="ai",
    )

    result = score_lead(payload, qualification)

    assert result.score == 8
    assert result.tier == "cold"
    assert result.recommended_action == "Send automated nurture follow-up"


def test_score_is_capped_at_100() -> None:
    payload = LeadCreate(
        name="Sarah Miller",
        email="sarah@example.com",
        company="Bright Dental",
        message=(
            "Urgent: we need a full website redesign this week and want a proposal today. "
            "We are ready to start immediately."
        ),
    )
    qualification = QualificationResult(
        service_type="website_development",
        intent="high",
        urgency="high",
        summary="Urgent website redesign.",
        language="en",
        source="ai",
    )

    result = score_lead(payload, qualification)

    assert result.score == 100
