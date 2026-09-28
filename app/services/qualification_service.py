from __future__ import annotations

from dataclasses import dataclass

from app.integrations.llm import LLMProvider, OpenAICompatibleProvider
from app.schemas.lead import LeadCreate, LeadQualification

ALLOWED_INTENT = {"low", "medium", "high", "unknown"}
ALLOWED_URGENCY = {"low", "medium", "high", "unknown"}

SYSTEM_PROMPT = '''
You qualify inbound SMB sales leads.

Return exactly one JSON object with these keys:
- service_type
- intent
- urgency
- summary
- language

Rules:
- intent must be one of: low, medium, high, unknown
- urgency must be one of: low, medium, high, unknown
- service_type should be a short snake_case label
- summary must be factual and concise
- language should be a short language code when clear, otherwise "unknown"
- never invent facts that are not present in the lead
'''.strip()


@dataclass(frozen=True)
class QualificationResult:
    service_type: str
    intent: str
    urgency: str
    summary: str
    language: str
    source: str

    def to_schema(self) -> LeadQualification:
        return LeadQualification(
            service_type=self.service_type,
            intent=self.intent,
            urgency=self.urgency,
            summary=self.summary,
            language=self.language,
            source=self.source,
        )


def _normalize_label(value: object, *, allowed: set[str]) -> str:
    normalized = str(value or "").strip().lower()
    return normalized if normalized in allowed else "unknown"


def _safe_text(value: object, *, default: str, max_length: int) -> str:
    text = str(value or "").strip()
    return (text or default)[:max_length]


def _fallback_qualification(payload: LeadCreate) -> QualificationResult:
    message = payload.message.strip()
    lowered = message.lower()

    urgency_tokens = ("urgent", "asap", "this week", "next week", "next month")
    urgency = "high" if any(token in lowered for token in urgency_tokens) else "unknown"

    intent = "medium"
    if any(token in lowered for token in ("need", "want", "looking for", "quote", "proposal")):
        intent = "high"

    language = "en" if message.isascii() else "unknown"

    return QualificationResult(
        service_type="unknown",
        intent=intent,
        urgency=urgency,
        summary=message[:240],
        language=language,
        source="fallback",
    )


def qualify_lead(
    payload: LeadCreate,
    provider: LLMProvider | None = None,
) -> QualificationResult:
    provider = provider or OpenAICompatibleProvider()

    user_prompt = (
        f"Name: {payload.name}\n"
        f"Company: {payload.company or 'N/A'}\n"
        f"Message: {payload.message}"
    )

    try:
        raw = provider.complete_json(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        service_type = _safe_text(
            raw.get("service_type"),
            default="unknown",
            max_length=64,
        ).lower().replace(" ", "_")

        return QualificationResult(
            service_type=service_type,
            intent=_normalize_label(raw.get("intent"), allowed=ALLOWED_INTENT),
            urgency=_normalize_label(raw.get("urgency"), allowed=ALLOWED_URGENCY),
            summary=_safe_text(raw.get("summary"), default=payload.message, max_length=500),
            language=_safe_text(
                raw.get("language"),
                default="unknown",
                max_length=16,
            ).lower(),
            source="ai",
        )
    except (RuntimeError, ValueError, KeyError, TypeError):
        return _fallback_qualification(payload)
    except Exception:
        return _fallback_qualification(payload)
