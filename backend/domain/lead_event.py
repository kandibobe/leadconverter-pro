from datetime import datetime
from typing import Any, Dict
from pydantic import BaseModel


class LeadEventBase(BaseModel):
    lead_id: int
    event_type: str
    payload: Dict[str, Any]


class LeadEventCreate(LeadEventBase):
    pass


class LeadEventOut(LeadEventBase):
    id: int
    tenant_id: str
    created_at: datetime

    class Config:
        from_attributes = True
