from pydantic import BaseModel, EmailStr, Field


class LeadCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    company: str | None = Field(default=None, max_length=160)
    message: str = Field(min_length=5, max_length=5000)


class LeadResponse(BaseModel):
    id: int
    status: str
    duplicate: bool
