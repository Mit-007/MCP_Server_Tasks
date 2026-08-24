from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    error: str = Field(...,description="Human-readable description of the error")
    code: str = Field(...,description="Machine-readable error code")
    suggestion: str = Field(...,description="Suggested action to resolve or handle the error")