from app.schemas.lead import LeadCreate
from app.services.qualification_service import QualificationResult
from app.services.scoring_service import ScoringResult


def build_followup_draft(
    payload: LeadCreate,
    qualification: QualificationResult,
    scoring: ScoringResult,
) -> str:
    first_name = payload.name.strip().split()[0]
    service = qualification.service_type.replace("_", " ")

    if qualification.service_type == "unknown":
        service_phrase = "your request"
    else:
        service_phrase = f"your {service} project"

    if scoring.tier == "hot":
        next_step = "I'd be happy to discuss the scope and timeline with you as soon as possible."
    elif scoring.tier == "warm":
        next_step = "I'd be happy to review the details and suggest the best next step."
    else:
        next_step = "I'd be happy to share more information and answer any questions you have."

    return (
        f"Hi {first_name},\n\n"
        f"Thanks for reaching out about {service_phrase}. "
        f"{next_step}\n\n"
        "Best regards,\n"
        "AIA Studio"
    )
