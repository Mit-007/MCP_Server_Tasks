from pydantic import BaseModel

from src.tasks_mcp_server.task_3.call_log_server.schemas.call_schemas import (
    Call,
    CallNote
)

# -> log_call
class LogCallOutput(BaseModel):
    data: Call

# -> get_call 
class GetCallOutput(BaseModel):
    data: Call

# -> list_calls , lost_calls_by_status
class CallsOutput(BaseModel):
    data: list[Call]
    next_cursor: str | None = None
    has_more: bool
    total_count: int

# -> update_call_outcome
class UpdateCallOutcomeOutput(BaseModel):
    data: Call

# -> delete_call
class DeleteCallOutput(BaseModel):
    data: bool

# -> add_call_note
class AddCallNoteOutput(BaseModel):
    data: CallNote

# -> list_notes_for_call
class NotesOutput(BaseModel):
    data: list[CallNote]
    next_cursor: str | None = None
    has_more: bool
    total_count: int

# -> get_call_summary
class CallSummaryOutput(BaseModel):
    data: str

# -> get_stats
class StatusStats(BaseModel):
    pending: int = 0
    in_progress: int = 0
    completed: int = 0
    failed: int = 0
    cancelled: int = 0


class OutcomeStats(BaseModel):
    resolved: int = 0
    unresolved: int = 0
    escalated: int = 0
    follow_up_required: int = 0
    no_answer: int = 0


class StatsData(BaseModel):
    total_calls: int
    by_status: StatusStats
    by_outcome: OutcomeStats


class StatsOutput(BaseModel):
    data: StatsData