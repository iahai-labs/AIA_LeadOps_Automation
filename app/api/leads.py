from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.lead import LeadCreate, LeadResponse
from app.services.lead_service import create_lead

router = APIRouter(prefix="/leads", tags=["leads"])
DbSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
def receive_lead(payload: LeadCreate, db: DbSession) -> LeadResponse:
    return create_lead(db, payload)
