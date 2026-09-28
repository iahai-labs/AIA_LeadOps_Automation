import json

from sqlalchemy.orm import Session

from app.repositories.audit_repository import record_event


def audit(
    db: Session,
    *,
    lead_id: int,
    event_type: str,
    payload: dict[str, object],
) -> None:
    record_event(
        db,
        lead_id=lead_id,
        event_type=event_type,
        event_data=json.dumps(payload, ensure_ascii=False, sort_keys=True),
    )
