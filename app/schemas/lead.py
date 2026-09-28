from pydantic import BaseModel, EmailStr, Field


class LeadCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    company: str | None = Field(default=None, max_length=160)
    message: str = Field(min_length=5, max_length=5000)


class LeadQualification(BaseModel):
    service_type: str
    intent: str
    urgency: str
    summary: str
    language: str
    source: str


class LeadScoring(BaseModel):
    score: int = Field(ge=0, le=100)
    tier: str
    recommended_action: str
    reasons: list[str]


class LeadResponse(BaseModel):
    id: int
    status: str
    duplicate: bool
    qualification: LeadQualification
    scoring: LeadScoring
