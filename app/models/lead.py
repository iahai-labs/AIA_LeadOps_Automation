from datetime import UTC, datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(320), index=True)
    company: Mapped[str | None] = mapped_column(String(160), nullable=True)
    message: Mapped[str] = mapped_column(Text)
    fingerprint: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(32), default="received")

    service_type: Mapped[str] = mapped_column(String(64), default="unknown")
    intent: Mapped[str] = mapped_column(String(16), default="unknown")
    urgency: Mapped[str] = mapped_column(String(16), default="unknown")
    qualification_summary: Mapped[str] = mapped_column(Text, default="")
    language: Mapped[str] = mapped_column(String(16), default="unknown")
    qualification_source: Mapped[str] = mapped_column(String(24), default="fallback")

    lead_score: Mapped[int] = mapped_column(Integer, default=0)
    lead_tier: Mapped[str] = mapped_column(String(16), default="cold")
    recommended_action: Mapped[str] = mapped_column(String(160), default="")
    score_reasons: Mapped[str] = mapped_column(Text, default="[]")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )
