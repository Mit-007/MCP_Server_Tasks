from pydantic import BaseModel

#  job schema for return job , job list
class Job(BaseModel):
    id: str
    title: str
    status: str
    description: str
    priority: str
    technician_id: str | None

# for technicians chemas
class Technician(BaseModel):
    id: str
    name: str
    available: bool
    skills: list[str]

# list_job_tool
class JobsOutput(BaseModel):
    jobs: list[Job]

# list_technicians_tools
class TechniciansOutput(BaseModel):
    technicians: list[Technician]

# for all write tools
class JobMutationResponse(BaseModel):
    success: bool
    message: str
    job: Job | None