from pydantic import BaseModel,Field 
from enum import Enum
from typing import Optional

# --> Input schema for a tools:
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class JobStatus(str, Enum):
    OPEN = "open"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class CreateJobInput(BaseModel):
    id: str = Field(..., description="Unique identifier for the job", min_length=3)
    title: str = Field(..., description="Job title", min_length=1, max_length=200)
    description: str = Field(..., description="Detailed job description", min_length=1, max_length=2000)
    priority: Priority = Field(..., description="Job priority level")


class AssignJobInput(BaseModel):
    job_id: str = Field(..., description="ID of the job to assign", min_length=3)
    technician_id: str = Field(..., description="ID of the technician to assign", min_length=3)


class UpdateJobInput(BaseModel):
    job_id: str = Field(..., description="ID of the job to update", min_length=3)
    title: Optional[str] = Field(None, description="Updated job title", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="Updated job description", min_length=1, max_length=2000)
    priority: Optional[Priority] = Field(None,description="Updated priority level",)
    status: Optional[JobStatus] = Field(None,description="Updated job status",)
    technician_id: Optional[str] = Field(None, description="ID of assigned technician", min_length=3)


class DeleteJobInput(BaseModel):
    job_id: str = Field(..., description="ID of the job to delete", min_length=3)