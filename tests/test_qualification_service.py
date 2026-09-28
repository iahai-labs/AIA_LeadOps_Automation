from app.schemas.lead import LeadCreate
from app.services.qualification_service import qualify_lead


class FakeProvider:
    def complete_json(self, *, system_prompt: str, user_prompt: str) -> dict[str, object]:
        assert "qualify inbound SMB sales leads" in system_prompt
        assert "Bright Dental" in user_prompt
        return {
            "service_type": "website_development",
            "intent": "high",
            "urgency": "high",
            "summary": "Dental clinic needs a website next month.",
            "language": "en",
        }


class BrokenProvider:
    def complete_json(self, *, system_prompt: str, user_prompt: str) -> dict[str, object]:
        raise RuntimeError("provider unavailable")


def make_payload() -> LeadCreate:
    return LeadCreate(
        name="Sarah Miller",
        email="sarah@example.com",
        company="Bright Dental",
        message="We need a new website for our dental clinic next month.",
    )


def test_ai_qualification_is_normalized() -> None:
    result = qualify_lead(make_payload(), provider=FakeProvider())

    assert result.service_type == "website_development"
    assert result.intent == "high"
    assert result.urgency == "high"
    assert result.language == "en"
    assert result.source == "ai"


def test_provider_failure_uses_safe_fallback() -> None:
    result = qualify_lead(make_payload(), provider=BrokenProvider())

    assert result.source == "fallback"
    assert result.intent == "high"
    assert result.urgency == "high"
    assert result.summary
