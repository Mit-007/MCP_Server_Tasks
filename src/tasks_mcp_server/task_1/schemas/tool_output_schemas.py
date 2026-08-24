from pydantic import BaseModel

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

class JobsOutput(BaseModel):
    jobs: list[Job]

class TechniciansOutput(BaseModel):
    technicians: list[Technician]

class JobOutput(BaseModel):
    job: Job | None

class JobMutationResponse(BaseModel):
    success: bool
    message: str
    job: Job | None