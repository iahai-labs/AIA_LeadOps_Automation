from dataclasses import dataclass

from app.schemas.lead import LeadCreate, LeadScoring
from app.services.qualification_service import QualificationResult

INTENT_POINTS = {
    "high": 40,
    "medium": 20,
    "low": 5,
    "unknown": 0,
}

URGENCY_POINTS = {
    "high": 25,
    "medium": 12,
    "low": 3,
    "unknown": 0,
}

TIMELINE_TOKENS = (
    "today",
    "tomorrow",
    "this week",
    "next week",
    "next month",
    "asap",
    "urgent",
)


@dataclass(frozen=True)
class ScoringResult:
    score: int
    tier: str
    recommended_action: str
    reasons: list[str]

    def to_schema(self) -> LeadScoring:
        return LeadScoring(
            score=self.score,
            tier=self.tier,
            recommended_action=self.recommended_action,
            reasons=self.reasons,
        )


def _tier_for_score(score: int) -> tuple[str, str]:
    if score >= 75:
        return "hot", "Contact within 4 hours"
    if score >= 45:
        return "warm", "Contact within 1 business day"
    return "cold", "Send automated nurture follow-up"


def score_lead(
    payload: LeadCreate,
    qualification: QualificationResult,
) -> ScoringResult:
    score = 0
    reasons: list[str] = []

    intent_points = INTENT_POINTS.get(qualification.intent, 0)
    score += intent_points
    if intent_points:
        reasons.append(f"Intent '{qualification.intent}' contributed {intent_points} points")

    urgency_points = URGENCY_POINTS.get(qualification.urgency, 0)
    score += urgency_points
    if urgency_points:
        reasons.append(
            f"Urgency '{qualification.urgency}' contributed {urgency_points} points"
        )

    if qualification.service_type != "unknown":
        score += 15
        reasons.append("Recognized service need contributed 15 points")

    if payload.company:
        score += 5
        reasons.append("Company information contributed 5 points")

    message_length = len(payload.message.strip())
    if message_length >= 60:
        score += 5
        reasons.append("Detailed lead message contributed 5 points")
    elif message_length >= 20:
        score += 3
        reasons.append("Useful lead message contributed 3 points")

    lowered = payload.message.lower()
    if any(token in lowered for token in TIMELINE_TOKENS):
        score += 10
        reasons.append("Explicit timeline signal contributed 10 points")

    final_score = min(score, 100)
    tier, recommended_action = _tier_for_score(final_score)

    return ScoringResult(
        score=final_score,
        tier=tier,
        recommended_action=recommended_action,
        reasons=reasons,
    )
