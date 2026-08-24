from datetime import datetime
from pydantic import BaseModel, Field
from src.tasks_mcp_server.task_3.call_log_server.schemas.call_schemas import (CallOutcome,CallStatus)

# pagination 
# -> tool : list_calls
class PaginationInput(BaseModel):
    cursor: str | None = None
    limit: int = Field(default=10, ge=1, le=100)

# -> log_call
class LogCallInput(BaseModel):
    customer_name: str
    phone_number: str
    agent_name: str
    started_at: datetime
    duration_seconds: int = Field(default=0,ge=0,)
    status: CallStatus
    outcome: CallOutcome | None = None
    transcript: str | None = None

# -> get_call
class GetCallInput(BaseModel):
    call_id: str

# -> list_calls_by_status
class CallsByStatusInput(PaginationInput):
    status: CallStatus

# -> update_call_outcome
class UpdateCallOutcomeInput(BaseModel):
    call_id: str
    outcome: CallOutcome

# -> delete_call
class DeleteCallInput(BaseModel):
    call_id: str

# -> add_call_note
class AddCallNoteInput(BaseModel):
    call_id: str
    text: str = Field(min_length=1)

# -> list_notes_for_call
class ListNotesInput(PaginationInput):
    call_id: str

# -> get_call_summary
class GetCallSummaryInput(BaseModel):
    call_id: str