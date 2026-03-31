from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum

class TicketStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"

class TicketCreate(BaseModel):
    title: str
    description: str

    model_config = ConfigDict(extra="forbid")


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    created_by_user_university_id: str
    created_by_user_name: str
    assigned_to_user_name: str
    status: TicketStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TicketUpdate(BaseModel):
    status: TicketStatus | None=None

    model_config = ConfigDict(extra="forbid")
