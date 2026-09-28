import json
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.audit_repository import list_events_for_lead
from app.schemas.lead import (
    LeadAuditEvent,
    LeadAuditResponse,
    LeadCreate,
    LeadDetailResponse,
    LeadResponse,
)
from app.services.lead_service import create_lead, get_lead_detail

router = APIRouter(prefix="/leads", tags=["leads"])
DbSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
def receive_lead(payload: LeadCreate, db: DbSession) -> LeadResponse:
    return create_lead(db, payload)


@router.get("/{lead_id}", response_model=LeadDetailResponse)
def get_lead(lead_id: int, db: DbSession) -> LeadDetailResponse:
    lead = get_lead_detail(db, lead_id)
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.get("/{lead_id}/audit", response_model=LeadAuditResponse)
def get_lead_audit(lead_id: int, db: DbSession) -> LeadAuditResponse:
    lead = get_lead_detail(db, lead_id)
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")

    events = []
    for event in list_events_for_lead(db, lead_id):
        try:
            event_data = json.loads(event.event_data)
        except json.JSONDecodeError:
            event_data = {}

        if not isinstance(event_data, dict):
            event_data = {}

        events.append(
            LeadAuditEvent(
                id=event.id,
                event_type=event.event_type,
                event_data=event_data,
            )
        )

    return LeadAuditResponse(lead_id=lead_id, events=events)
