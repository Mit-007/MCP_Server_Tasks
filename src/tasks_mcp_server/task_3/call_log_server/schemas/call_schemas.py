from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class CallStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class CallOutcome(str, Enum):
    RESOLVED = "resolved"
    UNRESOLVED = "unresolved"
    ESCALATED = "escalated"
    FOLLOW_UP_REQUIRED = "follow_up_required"
    NO_ANSWER = "no_answer"

class CallNote(BaseModel):
    note_id: str
    text: str
    created_at: datetime


class Call(BaseModel):
    call_id: str

    customer_name: str

    phone_number: str

    agent_name: str

    started_at: datetime

    duration_seconds: int = Field(
        default=0,
        ge=0,
    )

    status: CallStatus

    outcome: CallOutcome | None = None

    transcript: str | None = None

    summary: str | None = None

    notes: list[CallNote] = Field(
        default_factory=list
    )