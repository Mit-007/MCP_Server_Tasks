from pydantic import BaseModel ,Field


class Job(BaseModel):
    id: str
    title: str
    status: str
    description: str
    priority: str
    technician_id: str | None

class Technician(BaseModel):
    id: str
    name: str
    available: bool
    skills: list[str]

class Pagination(BaseModel):
    next_cursor: str | None = None
    has_more: bool
    total_count: int

class JobsOutput(BaseModel):
    data: list[Job]
    next_cursor: str | None
    has_more: bool
    total_count: int

class TechniciansOutput(BaseModel):
    data: list[Technician]
    next_cursor: str | None
    has_more: bool
    total_count: int

class JobMutationResponse(BaseModel):
    success: bool
    message: str
    job: Job | None