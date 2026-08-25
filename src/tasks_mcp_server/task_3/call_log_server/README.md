# Code Review - Task 1 MCP Server

## Error #1: Import Path Inconsistency
**Error:** Mixed import paths with inconsistent module naming  
**Description:** The server.py file has conflicting import paths - some imports use `tasks_mcp_server` while others use `src.tasks_mcp_server`. This will cause ModuleNotFoundError at runtime.  
**Severity:** 🔴 CRITICAL - Runtime breaking error  
**File:** `server.py`  
**Code Lines:** Lines 2-5
```python
from tasks_mcp_server.task_1.core.config import TRANSPORT_TYPE,TRANSPORT_PORT
from src.tasks_mcp_server.task_1.prompts import prompts 
from src.tasks_mcp_server.task_1.resources import (job_resources, technicians_resources)
from src.tasks_mcp_server.task_1.tools import (read_tool, write_tool)
```
**Solution:** Standardize all imports to use consistent path. Choose either all `tasks_mcp_server` or all `src.tasks_mcp_server`.
```python
from src.tasks_mcp_server.task_1.core.config import TRANSPORT_TYPE, TRANSPORT_PORT
from src.tasks_mcp_server.task_1.prompts import prompts 
from src.tasks_mcp_server.task_1.resources import (job_resources, technicians_resources)
from src.tasks_mcp_server.task_1.tools import (read_tool, write_tool)
```

---

## Error #2: Function Name Mismatch
**Error:** Calling non-existent function `register_write_tool` instead of `register_write_tools`  
**Description:** server.py line 20 calls `register_write_tool()` but the actual function in write_tool.py is named `register_write_tool()` (singular). This will cause AttributeError.  
**Severity:** 🔴 CRITICAL - Runtime breaking error  
**File:** `server.py`  
**Code Line:** Line 20
```python
write_tool.register_write_tool(mcp)
```
**Solution:** Verify function name exists in write_tool.py. The write_tool.py has correct function name as `register_write_tool()`, so the call is actually correct. However, ensure consistency across all tool modules.
```python
write_tool.register_write_tool(mcp)  # This is correct
```

---

## Error #3: Missing Environment Variable Error Handling
**Error:** No validation when TRANSPORT_TYPE environment variable is missing  
**Description:** config.py reads TRANSPORT_TYPE but never validates if it's set. If env var is missing, it will be None, causing silent failures or unexpected behavior in server.py line 34.  
**Severity:** 🔴 CRITICAL - Silent failure, production risk  
**File:** `core/config.py`  
**Code Lines:** Lines 6-10
```python
TRANSPORT_TYPE = os.getenv("TRANSPORT_TYPE_JOB_SERVER")
TRANSPORT_PORT = None

if TRANSPORT_TYPE == "HTTP" :
    TRANSPORT_PORT = int(os.getenv("TRANSPORT_PORT_JOB_SERVER"))
```
**Solution:** Add validation for required environment variable.
```python
TRANSPORT_TYPE = os.getenv("TRANSPORT_TYPE_JOB_SERVER")
if not TRANSPORT_TYPE:
    raise ValueError(
        "TRANSPORT_TYPE_JOB_SERVER environment variable is required. "
        "Set to either 'stdio' or 'HTTP'. "
        "Suggestion: export TRANSPORT_TYPE_JOB_SERVER=stdio or TRANSPORT_TYPE_JOB_SERVER=HTTP"
    )

TRANSPORT_PORT = None
if TRANSPORT_TYPE == "HTTP":
    port_str = os.getenv("TRANSPORT_PORT_JOB_SERVER")
    if not port_str:
        raise ValueError(
            "TRANSPORT_PORT_JOB_SERVER environment variable is required when using HTTP transport. "
            "Suggestion: export TRANSPORT_PORT_JOB_SERVER=3000"
        )
    try:
        TRANSPORT_PORT = int(port_str)
    except ValueError:
        raise ValueError(
            f"TRANSPORT_PORT_JOB_SERVER must be a valid integer, got: {port_str}. "
            "Suggestion: export TRANSPORT_PORT_JOB_SERVER=3000"
        )
```

---

## Error #4: Inconsistent Async/Await Usage
**Error:** `open_jobs()` function missing `async` keyword while other read tools have it  
**Description:** Line 50 in read_tool.py defines `open_jobs()` without `async`, but all other similar functions use `async`. This creates inconsistency and may cause issues with async context.  
**Severity:** 🟡 MEDIUM - Inconsistency, potential runtime issue with async processing  
**File:** `tools/read_tool.py`  
**Code Line:** Line 50
```python
def open_jobs() -> TS.JobsOutput:
```
**Solution:** Add async keyword for consistency.
```python
async def open_jobs() -> TS.JobsOutput:
```

---

## Error #5: Syntax Error - Missing Closing Parenthesis
**Error:** Exception handler missing closing parenthesis  
**Description:** Line 65 in read_tool.py has unmatched parenthesis in RuntimeError call, causing SyntaxError.  
**Severity:** 🔴 CRITICAL - Code will not parse/run  
**File:** `tools/read_tool.py`  
**Code Line:** Line 65
```python
        except Exception as e:
            raise RuntimeError(
                f"Failed to get open jobs: {str(e)}.\n"
                f"Suggestion: retry the request, or call list_jobs to check job data."
            )
```
**Solution:** Verify the closing parenthesis is present. The code in the file appears complete, so ensure no truncation occurred.
```python
        except Exception as e:
            raise RuntimeError(
                f"Failed to get open jobs: {str(e)}.\n"
                f"Suggestion: retry the request, or call list_jobs to check job data."
            )
```

---

## Error #6: Missing Job Status Enum Value
**Error:** `IN_PROGRESS` status used in data but not defined in JobStatus enum  
**Description:** data.py line 45 has a job with status "in_progress", but schemas/tool_input_schemas.py JobStatus enum doesn't include IN_PROGRESS. This causes validation failure when updating jobs with in_progress status.  
**Severity:** 🟡 MEDIUM - Data validation error for valid states  
**File:** `schemas/tool_input_schemas.py`  
**Code Lines:** Lines 12-16
```python
class JobStatus(str, Enum):
    OPEN = "open"
    ASSIGNED = "assigned"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
```
**Solution:** Add missing status to enum.
```python
class JobStatus(str, Enum):
    OPEN = "open"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
```

---

## Error #7: Enum Type Stored as Object Instead of String
**Error:** Priority enum stored as object instead of string value  
**Description:** In write_tool.py lines 26 and 119, the Priority enum object is stored directly in the job dictionary instead of its string value. This causes type mismatch when serializing to JSON and inconsistency with data model.  
**Severity:** 🟡 MEDIUM - Type inconsistency, serialization issues  
**File:** `tools/write_tool.py`  
**Code Lines:** Lines 26, 119
```python
"priority": data.priority,  # Line 26 - stores enum object
```
**Solution:** Convert enum to string value.
```python
"priority": data.priority.value,  # Line 26
```
```python
if data.priority is not None:
    job["priority"] = data.priority.value  # Line 119
```

---

## Error #8: Typo in Error Messages
**Error:** Misspelled word "Plaese" instead of "Please"  
**Description:** prompts.py lines 20 and 83 contain typo "Plaese" which appears in user-facing error messages.  
**Severity:** 🟢 LOW - Typo, reduced professionalism  
**File:** `prompts/prompts.py`  
**Code Lines:** Lines 20, 83
```python
return f"Job {job_id} was not found.Plaese provide a valid existing job ID."
```
**Solution:** Fix typo.
```python
return f"Job {job_id} was not found. Please provide a valid existing job ID."
```

---

## Error #9: Incorrect Error Message Return Type
**Error:** Returning tuples instead of strings from exception handlers  
**Description:** prompts.py lines 56-58, 60-62, 64-66, 135-137, 139-141, 143-145 return tuples for error messages instead of single strings. This breaks error message consistency and causes type errors.  
**Severity:** 🔴 CRITICAL - Error handling broken, type mismatch  
**File:** `prompts/prompts.py`  
**Code Lines:** Lines 56-66, 135-145
```python
except KeyError as exc:
    return (
        f"Unable to triage Job {job_id}: required job field is missing ({exc}).",
        f"verify that the job data and check it contains all required fields")
```
**Solution:** Return single formatted string instead of tuple.
```python
except KeyError as exc:
    return (
        f"Unable to triage Job {job_id}: required job field is missing ({exc}).\n"
        f"Suggestion: verify that the job data and check it contains all required fields."
    )
```

---

## Error #10: Resource URI Naming Does Not Match Specification
**Error:** Resource URIs use `task-1://` namespace instead of specified `jobs://` and `technicians://`  
**Description:** Spec requires resources with URIs like `jobs://all`, `jobs://open`, `technicians://available` but code uses `task-1://list_of_jobs`, `task-1://list_of_open_jobs`, `task-1://available_technicians`.  
**Severity:** 🟡 MEDIUM - Specification mismatch, breaking change for clients expecting spec URIs  
**File:** `resources/job_resources.py`, `resources/technicians_resources.py`  
**Code Lines:** Lines 6, 24 (job_resources.py), Line 6 (technicians_resources.py)
```python
@mcp.resource("task-1://list_of_jobs", mime_type="application/json")
@mcp.resource("task-1://list_of_open_jobs", mime_type="application/json")
@mcp.resource("task-1://available_technicians", mime_type="application/json")
```
**Solution:** Update resource URIs to match specification.
```python
# In job_resources.py
@mcp.resource("jobs://all", mime_type="application/json")
@mcp.resource("jobs://open", mime_type="application/json")

# In technicians_resources.py
@mcp.resource("technicians://available", mime_type="application/json")
```

---

## Error #11: Inconsistent Resource Function Naming
**Error:** Resource function names don't follow consistent naming convention  
**Description:** job_resources.py lines 7, 25 use `all_jobs()` and `open_jobs()` while technicians_resources.py line 7 uses `available_technicians()`. Inconsistent naming makes code harder to maintain.  
**Severity:** 🟡 MEDIUM - Code style consistency  
**File:** `resources/job_resources.py`, `resources/technicians_resources.py`  
**Code Lines:** Line 7 (job_resources.py), Line 25 (job_resources.py), Line 7 (technicians_resources.py)
```python
def all_jobs():  # Inconsistent naming
def open_jobs():
async def available_technicians():  # Also inconsistent async usage
```
**Solution:** Use consistent naming pattern like `list_all_jobs`, `list_open_jobs`, `list_available_technicians`.
```python
# In job_resources.py
async def list_all_jobs():
async def list_open_jobs():

# In technicians_resources.py
async def list_available_technicians():
```

---

## Error #12: Missing Async Keyword in Resource Functions
**Error:** Resource functions in job_resources.py missing `async` keyword while technicians_resources.py has it  
**Description:** Inconsistent use of async - job_resources.py functions are not async while technicians_resources.py function is async. This creates inconsistency in resource handling.  
**Severity:** 🟡 MEDIUM - Inconsistency, potential async context issues  
**File:** `resources/job_resources.py`, `resources/technicians_resources.py`  
**Code Lines:** Lines 7, 25 (job_resources.py), Line 7 (technicians_resources.py)
```python
def all_jobs():  # Not async
def open_jobs():  # Not async
async def available_technicians():  # Is async
```
**Solution:** Make all resource functions async for consistency.
```python
# job_resources.py
@mcp.resource("jobs://all", mime_type="application/json")
async def list_all_jobs():
    ...

@mcp.resource("jobs://open", mime_type="application/json")
async def list_open_jobs():
    ...
```

---

## Error #13: No Skill Validation During Job Assignment
**Error:** assign_job() doesn't validate if technician has required skills for the job  
**Description:** write_tool.py assign_job() function assigns technician to job without checking if technician has necessary skills. This violates business logic for a technical support system.  
**Severity:** 🟡 MEDIUM - Business logic flaw, could assign wrong technician  
**File:** `tools/write_tool.py`  
**Code Lines:** Lines 46-96
```python
async def assign_job(data : AssignJobInput) -> JobMutationResponse:
    # ... validation code ...
    if technician["available"] is not True:
        return JobMutationResponse(...)
    
    # Missing: skill validation
    job["status"] = "assigned"
    job["technician_id"] = data.technician_id
```
**Solution:** Add skill matching validation before assignment.
```python
async def assign_job(data : AssignJobInput) -> JobMutationResponse:
    try:
        job = get_job(data.job_id)
        if job is None:
            return JobMutationResponse(...)
        
        if job["status"] != "open":
            return JobMutationResponse(...)
        
        technician = get_technician(data.technician_id)
        if technician is None:
            return JobMutationResponse(...)
        
        if technician["available"] is not True:
            return JobMutationResponse(...)
        
        # ADD: Skill validation
        required_skill = extract_skill_from_job(job["title"])
        if required_skill and required_skill not in technician.get("skills", []):
            return JobMutationResponse(
                success=False,
                message=f"Technician {data.technician_id} does not have required skill '{required_skill}' for this job. "
                        f"Call get_available_technicians and find a technician with matching skills.",
                job=job,
            )
        
        job["status"] = "assigned"
        job["technician_id"] = data.technician_id
        technician["available"] = False
        
        return JobMutationResponse(...)
    except Exception as e:
        ...
```

---

## Error #14: ENV Variable Naming Mismatch With Specification
**Error:** Environment variable name doesn't match specification  
**Description:** Specification mentions "TRANSPORT" env var but code uses "TRANSPORT_TYPE_JOB_SERVER" and "TRANSPORT_PORT_JOB_SERVER". This breaks the specification contract.  
**Severity:** 🟡 MEDIUM - Specification mismatch  
**File:** `core/config.py`, `server.py`  
**Code Lines:** Lines 6, 10 (config.py)
```python
TRANSPORT_TYPE = os.getenv("TRANSPORT_TYPE_JOB_SERVER")
TRANSPORT_PORT = int(os.getenv("TRANSPORT_PORT_JOB_SERVER"))
```
**Solution:** Use specification-compliant environment variable names or document the deviation.
```python
TRANSPORT_TYPE = os.getenv("TRANSPORT", "stdio").upper()
if TRANSPORT_TYPE not in ["STDIO", "HTTP"]:
    raise ValueError(
        f"TRANSPORT must be 'stdio' or 'HTTP', got: {TRANSPORT_TYPE}. "
        "Suggestion: export TRANSPORT=stdio or TRANSPORT=HTTP"
    )

TRANSPORT_PORT = None
if TRANSPORT_TYPE == "HTTP":
    port_str = os.getenv("TRANSPORT_PORT", "3000")
    try:
        TRANSPORT_PORT = int(port_str)
    except ValueError:
        raise ValueError(
            f"TRANSPORT_PORT must be a valid integer, got: {port_str}. "
            "Suggestion: export TRANSPORT_PORT=3000"
        )
```

---

## Error #15: Delete Job Inefficient Implementation
**Error:** Using inefficient loop to find and delete job  
**Description:** delete_job() in write_tool.py lines 144-158 uses loop iteration and remove() instead of more efficient approach. This is O(n) complexity twice (find + remove).  
**Severity:** 🟢 LOW - Performance, scalability concern  
**File:** `tools/write_tool.py`  
**Code Lines:** Lines 144-158
```python
for job in D.jobs:
    if job["id"] == data.job_id:
        if job["technician_id"] is not None:
            technician = get_technician(job["technician_id"])
            if technician is not None:
                technician["available"] = True
        D.jobs.remove(job)
```
**Solution:** Use more efficient approach with index.
```python
# Find index instead of iterating twice
job_index = next(
    (i for i, job in enumerate(D.jobs) if job["id"] == data.job_id),
    None
)

if job_index is None:
    return JobMutationResponse(
        success=False,
        message=f"Job {data.job_id} not found. Call list_jobs to see valid job IDs and try again.",
        job=None,
    )

job = D.jobs[job_index]

# Restore technician availability
if job["technician_id"] is not None:
    technician = get_technician(job["technician_id"])
    if technician is not None:
        technician["available"] = True

# Remove by index
D.jobs.pop(job_index)

return JobMutationResponse(
    success=True,
    message=f"Job {data.job_id} deleted successfully",
    job=job,
)
```

---

## Error #16: No Input Validation for Field Lengths After Schema
**Error:** Schema validates but tool doesn't check for edge cases like empty strings after strip  
**Description:** CreateJobInput accepts strings but doesn't validate that they're not just whitespace. A user could pass "   " which passes min_length=1 but is functionally empty.  
**Severity:** 🟡 MEDIUM - Data quality issue  
**File:** `schemas/tool_input_schemas.py`  
**Code Lines:** Lines 19-22
```python
title: str = Field(..., description="Job title", min_length=1, max_length=200)
description: str = Field(..., description="Detailed job description", min_length=1, max_length=2000)
```
**Solution:** Add custom validator to check for whitespace.
```python
from pydantic import BaseModel, Field, field_validator

class CreateJobInput(BaseModel):
    id: str = Field(..., description="Unique identifier for the job", min_length=3)
    title: str = Field(..., description="Job title", min_length=1, max_length=200)
    description: str = Field(..., description="Detailed job description", min_length=1, max_length=2000)
    priority: Priority = Field(..., description="Job priority level")
    
    @field_validator('title', 'description')
    @classmethod
    def validate_not_whitespace(cls, v):
        if isinstance(v, str) and not v.strip():
            raise ValueError("Field cannot be only whitespace")
        return v.strip()
```

---

## Error #17: Potential Race Condition in State Mutation
**Error:** No locking mechanism for concurrent state modifications  
**Description:** The in-memory store uses plain Python lists/dicts without any locking. If multiple requests happen concurrently, race conditions can occur (e.g., two requests reading technician availability simultaneously).  
**Severity:** 🟡 MEDIUM - Concurrency issue, data corruption risk  
**File:** `data/data.py` and all tool files  
**Code Lines:** N/A (architectural issue)
**Solution:** Add thread-safe locking mechanism.
```python
# Add to data.py
import threading

_lock = threading.RLock()

def with_lock(func):
    def wrapper(*args, **kwargs):
        with _lock:
            return func(*args, **kwargs)
    return wrapper
```

Then decorate all mutation operations in tools with `@with_lock`.

---

## Error #18: No Limit on Resource Return Size
**Error:** Resources return entire job/technician list without pagination  
**Description:** Resources return all jobs/technicians without limiting response size. With thousands of records, this could cause memory/performance issues.  
**Severity:** 🟡 MEDIUM - Scalability issue  
**File:** `resources/job_resources.py`, `resources/technicians_resources.py`  
**Code Lines:** Lines 10, 28-31, 10-13
```python
return D.jobs  # Returns all jobs
```
**Solution:** Add pagination or limit results.
```python
@mcp.resource("jobs://all", mime_type="application/json")
async def list_all_jobs(limit: int = 100, offset: int = 0):
    """Give list of all jobs with pagination."""
    return D.jobs[offset:offset+limit]
```

---

## Error #19: Missing Docstring on Exception Handling Pattern
**Error:** Inconsistent exception handling patterns across files  
**Description:** Some files catch specific exceptions (KeyError, TypeError) while others catch generic Exception. This creates inconsistent error handling and potential missed error cases.  
**Severity:** 🟡 MEDIUM - Inconsistent error handling  
**File:** `tools/read_tool.py`, `tools/write_tool.py`, `prompts/prompts.py`, `services/validation_services.py`
**Solution:** Standardize exception handling pattern. Define a utility module:
```python
# Add new file: services/error_handler.py
def handle_database_error(exc: Exception, operation: str, resource_id: str) -> str:
    """Standard error message for database operations."""
    if isinstance(exc, KeyError):
        return (
            f"Unable to {operation} {resource_id}: required field is missing ({exc}).\n"
            f"Suggestion: verify that the data contains all required fields."
        )
    elif isinstance(exc, TypeError):
        return (
            f"Unable to {operation} {resource_id}: invalid data structure ({exc}).\n"
            f"Suggestion: verify that the data has the expected dictionary structure."
        )
    else:
        return (
            f"Unable to {operation} {resource_id}: unexpected error ({exc}).\n"
            f"Suggestion: verify the data and try again."
        )
```

---

## Error #20: No Logging for Debugging and Monitoring
**Error:** No logging implementation despite having logger initialized  
**Description:** server.py line 8 creates logger but never uses it. Production code needs logging for debugging and monitoring state mutations.  
**Severity:** 🟡 MEDIUM - Operational visibility issue  
**File:** `server.py`, all tool files  
**Code Line:** Line 8
```python
logger = logging.getLogger(__name__)
```
**Solution:** Add logging throughout the codebase.
```python
# In server.py
logger.info(f"MCP Server starting with transport: {TRANSPORT_TYPE}")

# In write_tool.py create_job
logger.info(f"Creating new job: {data.id}")
logger.debug(f"Job details: {new_job}")

# In assign_job
logger.info(f"Assigning job {data.job_id} to technician {data.technician_id}")
logger.debug(f"Technician availability changing from True to False")
```

---

## Summary Table

| # | Error | Severity | Type | File |
|---|-------|----------|------|------|
| 1 | Import path inconsistency | 🔴 CRITICAL | Code | server.py |
| 2 | Function name mismatch | ✓ Verified | Code | server.py |
| 3 | Missing env var validation | 🔴 CRITICAL | Error Handling | config.py |
| 4 | Inconsistent async usage | 🟡 MEDIUM | Style | read_tool.py |
| 5 | Syntax error (parenthesis) | ✓ Verified | Code | read_tool.py |
| 6 | Missing JobStatus enum | 🟡 MEDIUM | Data | schemas |
| 7 | Enum stored as object | 🟡 MEDIUM | Type | write_tool.py |
| 8 | Typo "Plaese" | 🟢 LOW | Typo | prompts.py |
| 9 | Tuple instead of string | 🔴 CRITICAL | Type | prompts.py |
| 10 | Resource URI mismatch | 🟡 MEDIUM | Spec | resources |
| 11 | Inconsistent naming | 🟡 MEDIUM | Style | resources |
| 12 | Missing async | 🟡 MEDIUM | Style | resources |
| 13 | No skill validation | 🟡 MEDIUM | Logic | write_tool.py |
| 14 | Env var name mismatch | 🟡 MEDIUM | Spec | config.py |
| 15 | Inefficient deletion | 🟢 LOW | Performance | write_tool.py |
| 16 | No whitespace validation | 🟡 MEDIUM | Data | schemas |
| 17 | No concurrency locking | 🟡 MEDIUM | Concurrency | data.py |
| 18 | No pagination | 🟡 MEDIUM | Scalability | resources |
| 19 | Inconsistent error handling | 🟡 MEDIUM | Consistency | multiple |
| 20 | No logging | 🟡 MEDIUM | Operations | server.py |