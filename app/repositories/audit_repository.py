from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.audit_event import AuditEvent


def record_event(
    db: Session,
    *,
    lead_id: int,
    event_type: str,
    event_data: str,
) -> AuditEvent:
    event = AuditEvent(
        lead_id=lead_id,
        event_type=event_type,
        event_data=event_data,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def list_events_for_lead(db: Session, lead_id: int) -> list[AuditEvent]:
    statement = (
        select(AuditEvent)
        .where(AuditEvent.lead_id == lead_id)
        .order_by(AuditEvent.id.asc())
    )
    return list(db.scalars(statement))
