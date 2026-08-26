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

#  pagination output 
class Pagination(BaseModel):
    next_cursor: str | None = None
    has_more: bool
    total_count: int

# list of jobs_tool
class JobsOutput(BaseModel):
    data: list[Job]
    pagination: Pagination

# list of technicians_tool
class TechniciansOutput(BaseModel):
    data: list[Technician]
    pagination: Pagination

# response structure for write tools
class JobMutationResponse(BaseModel):
    success: bool
    message: str
    job: Job | None