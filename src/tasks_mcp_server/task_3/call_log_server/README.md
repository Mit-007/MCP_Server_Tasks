<div align="center">

# 🚀 Task 3 — Multi-Server MCP Agent

### 🔗 Orchestrated Field-Service Agent with Dual MCP Servers

A production-oriented **multi-server MCP agent** that connects both the **Job Server (Task 2)** and **Call Log Server** simultaneously, orchestrating complex cross-server workflows through intelligent tool routing, request correlation, and structured logging.

<p>
  <img src="https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12+">
  <img src="https://img.shields.io/badge/LangChain-Multi%20MCP-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white" alt="LangChain">
  <img src="https://img.shields.io/badge/MCP-Dual%20Server-6C47FF?style=for-the-badge" alt="MCP Dual Server">
  <img src="https://img.shields.io/badge/Google%20Gemini-LLM-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Google Gemini">
  <img src="https://img.shields.io/badge/Authentication-Bearer%20Token-FF6B6B?style=for-the-badge" alt="Bearer Token Auth">
  <img src="https://img.shields.io/badge/Async-AsyncIO-2D3748?style=for-the-badge" alt="AsyncIO">
</p>

<p>
  <strong>2 MCP Servers</strong> ·
  <strong>18 Total Tools</strong> ·
  <strong>5 Workflows</strong> ·
  <strong>Token Authentication</strong> ·
  <strong>Request Correlation</strong>
</p>

</div>

---

## 📌 Overview

This project is a **multi-server MCP agent** that demonstrates sophisticated orchestration between two independent MCP servers:

1. **Job Server (Task 2)** — 8 tools for managing jobs and technicians
2. **Call Log Server (Task 3 Part A)** — 10 tools for managing customer call logs

The agent uses:

- 🤖 LLM-powered tool selection (Claude / Google Gemini)
- 🔗 Intelligent tool routing via prefix-based addressing
- 🔄 Cross-server workflow orchestration (5 complex workflows)
- 📊 Request correlation with unique IDs
- ⏱️ Comprehensive latency and metrics tracking
- 🔐 Bearer token authentication for both servers
- 📝 Structured logging with redaction of sensitive data
- 🔀 Result merging for identical tool semantics

---

## 🧰 Technologies Used

| Technology | Purpose |
|:---|:---|
| 🐍 **Python 3.12** | Application runtime |
| 🤖 **LangChain** | LLM orchestration and tool binding |
| 🔌 **MCP (Model Context Protocol)** | Multi-server tool interface |
| 🧠 **Google Gemini / Claude** | Language model for tool selection |
| 🌱 **python-dotenv** | Environment configuration |
| ⚡ **asyncio** | Concurrent async operations |
| 📊 **JSON** | Structured logging and result format |

Standard library modules used include:

- `asyncio`
- `json`
- `time`
- `uuid`
- `logging`

---

## 🏗️ Architecture

### Two-Server Configuration

```
┌────────────────────────────────────────────────────────────┐
│                       User Input                           │
│                    (Chatbot CLI)                           │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │   Claude / Gemini LLM      │
        │   (Tool Selection Logic)   │
        └────────┬───────────────────┘
                 │
         ┌───────┴───────┐
         │               │
         ▼               ▼
    ┌─────────┐    ┌──────────┐
    │ Tool    │    │ Workflow │
    │ Router  │    │ Tools    │
    │         │    │          │
    └────┬────┘    └──────────┘
         │
    ┌────┴──────────────────────┐
    │                           │
    ▼                           ▼
┌─────────────┐        ┌──────────────────┐
│ Job Server  │        │ Call Log Server  │
│ (Task 2)    │        │ (Task 3 Part A)  │
│             │        │                  │
│ Port: 3001  │        │ Port: 3000       │
│             │        │                  │
│ 8 Tools     │        │ 10 Tools         │
│ 3 Resources │        │ 2 Resources      │
│ 2 Prompts   │        │ 1 Prompt         │
└─────────────┘        └──────────────────┘
    │                           │
    └───────────┬───────────────┘
                │
                ▼
         ┌────────────────┐
         │  Correlation   │
         │  & Logging     │
         │                │
         │ - request_id   │
         │ - latency_ms   │
         │ - response_size│
         │ - server_name  │
         │ - tool_name    │
         └────────────────┘
```

### Request Flow

```
User Query
    │
    ▼
┌──────────────────────────────────┐
│ LLM Decides If Tool Needed       │
└──────────┬───────────────────────┘
           │
    ┌──────┴──────┐
    │             │
    ▼             ▼
No Tool       Identifies Tool
    │             │
    │             ▼
    │      ┌────────────────────┐
    │      │ Route Based On     │
    │      │ Tool Prefix        │
    │      │                    │
    │      │ job_server_* →     │
    │      │ Job Server (3001)  │
    │      │                    │
    │      │ call_log_server_* →│
    │      │ Call Log (3000)    │
    │      │                    │
    │      │ wf* →              │
    │      │ Workflow Tools     │
    │      └────────┬───────────┘
    │              │
    │              ▼
    │      ┌──────────────────┐
    │      │ Add Auth Header  │
    │      │ Bearer Token     │
    │      └────────┬─────────┘
    │              │
    │              ▼
    │      ┌──────────────────┐
    │      │ Execute Tool     │
    │      │ Track Latency    │
    │      │ Log Request      │
    │      └────────┬─────────┘
    │              │
    └──────┬───────┘
           │
           ▼
    ┌───────────────┐
    │ Feed Result   │
    │ Back to LLM   │
    └───────┬───────┘
            │
            ▼
    ┌───────────────┐
    │ LLM Returns   │
    │ Final Answer  │
    └───────────────┘
```

---

## 📁 Project Structure

```text
task_3/
│
├── call_log_server/
│   ├── server.py                 # Call Log Server main entry point
│   ├── auth/                      # Token verification & scope auth
│   │   ├── token_auth.py
│   │   └── scope_auth.py
│   ├── middleware/                # HTTP request authentication
│   │   └── middleware.py
│   ├── tools/                     # 10 MCP tools
│   │   └── tools.py
│   ├── resources/                 # 2 MCP resources
│   │   └── resources.py
│   ├── prompts/                   # 1 MCP prompt
│   │   └── prompts.py
│   ├── schemas/                   # Pydantic input/output/error schemas
│   │   ├── tool_input_schemas.py
│   │   ├── tool_output_schemas.py
│   │   ├── call_schemas.py
│   │   └── error_schemas.py
│   ├── services/                  # Helper validation services
│   │   ├── call_services.py
│   │   └── validation_tools_annotation.py
│   ├── data/                      # In-memory data store
│   │   ├── calls_data.py
│   │   └── token.py
│   └── core/                      # Config, logging, constants
│       ├── config.py
│       ├── logger.py
│       └── constant.py
│
├── agent/
│   ├── main.py                    # Agent entry point & orchestrator
│   ├── mcp_clients.py             # Multi-server MCP client config
│   ├── core/
│   │   ├── config.py              # Agent configuration
│   │   ├── server_config.py       # Job/Call servers endpoint config
│   │   └── logger.py              # Agent logging setup
│   ├── services/
│   │   ├── llm.py                 # LLM (Gemini) initialization
│   │   ├── prompt.py              # System prompt & tool descriptions
│   │   ├── tools.py               # Tool registry & routing
│   │   └── workflows_tools.py     # Workflow tool wrapper
│   ├── schemas/
│   │   ├── workflow_schemas.py    # Workflow result schemas
│   │   └── workflows_tools_schemas.py
│   └── workflows/                 # 5 Cross-server workflows
│       ├── wf1_link_job_and_call.py
│       ├── wf2_failed_calls_bulk_update_jobs.py
│       ├── wf3_create_follow_up_jobs.py
│       ├── wf4_pending_calls_jobs_mapping.py
│       └── wf5_stats_report_generate.py
│
├── ARCHITECTURE.md                # System architecture diagrams
├── EVALUATION.xml                 # 10 evaluation questions in MCP format
└── README.md                      # This file
```

---

## 🔧 Call Log Server Tools

| Name | Type | Description |
|:---|:---|:---|
| `call_log_server_log_call` | 🔴 Write | Creates a new customer call log. |
| `call_log_server_get_call` | 🟢 Read | Retrieves a call by call_id. |
| `call_log_server_list_calls` | 🟢 Read | Lists all calls with cursor pagination. |
| `call_log_server_list_calls_by_status` | 🟢 Read | Lists calls filtered by status with pagination. |
| `call_log_server_update_call_outcome` | 🔴 Write | Updates a call's outcome. |
| `call_log_server_delete_call` | 🔴 Write | Deletes a call from the log. |
| `call_log_server_add_call_note` | 🔴 Write | Adds a note/annotation to a call. |
| `call_log_server_list_notes_for_call` | 🟢 Read | Lists all notes for a specific call. |
| `call_log_server_get_call_summary` | 🟢 Read | Generates LLM-powered summary (via MCP sampling). |
| `call_log_server_get_stats` | 🟢 Read | Returns call statistics aggregated by status/outcome. |

---

## 📚 Call Log Server Resources

| Name | Type | Description |
|:---|:---|:---|
| `calls://recent/{n}` | Resource | Returns the N most recent calls as JSON. |
| `calls://failed` | Resource | Returns all failed calls as JSON. |

---

## 🤖 Call Log Server Prompt

| Name | Type | Description |
|:---|:---|:---|
| `call_log_server_quality_review` | Prompt | Generates a structured quality review prompt for a specific call. |

---

## 🔄 Cross-Server Workflows

### Workflow 1: Link Job and Call
**File:** `wf1_link_job_and_call.py`

Creates a call, creates a related job, and links them via a call note.

```
log_call() → create_job() → add_call_note()
```

**Use Case:** Customer reports an issue via call; system creates job and links them.

---

### Workflow 2: Failed Calls Bulk Update Jobs
**File:** `wf2_failed_calls_bulk_update_jobs.py`

Fetches failed calls, extracts job IDs, and bulk-updates matching jobs.

```
list_calls_by_status(failed) → 
extract job IDs (LLM) → 
list_jobs() → 
update_job() [for each match]
```

**Use Case:** QA review finds failed calls; system cascades updates to linked jobs.

---

### Workflow 3: Create Follow-up Jobs
**File:** `wf3_create_follow_up_jobs.py`

Analyzes pending calls and auto-creates follow-up jobs.

```
list_calls_by_status(pending) → 
LLM analysis → 
create_job() [for each follow-up needed]
```

**Use Case:** Proactive job creation based on pending call analysis.

---

### Workflow 4: Pending Calls to Jobs Mapping
**File:** `wf4_pending_calls_jobs_mapping.py`

Maps pending calls to open jobs and suggests assignments.

```
list_calls_by_status(pending) → 
list_jobs(open) → 
LLM matching → 
assign_job()
```

**Use Case:** Automated dispatcher matching pending issues to available work.

---

### Workflow 5: Call and Job Statistics Report
**File:** `wf5_stats_report_generate.py`

Merges statistics from both servers for a unified report.

```
get_stats(job_server) + 
get_stats(call_log_server) → 
merge → 
formatted report
```

**Use Case:** Executive dashboard combining both systems' metrics.

---

## 🔐 Authentication & Authorization

### Bearer Token Authentication

Both servers require valid bearer tokens with appropriate scopes:

- **read** scope: Allows read-only operations (list, get, resources, prompts)
- **write** scope: Allows write operations (create, update, delete, assign)

### Token Registry

Tokens are stored in `/call_log_server/data/token.py`:

```python
TOKEN_REGISTRY = {
    "dddgN6MH20Kx9fjJ5W50JCDaKjpxsS1p": {
        "scopes": ["read", "write"],
        "expires_at": 1797700000,
    },
    "SuELT0bTa1o4nrAJbUnJ9MOemdmmDlMN": {
        "scopes": ["read"],
        "expires_at": 1797600000,
    },
}
```

### Header Format

```http
Authorization: Bearer dddgN6MH20Kx9fjJ5W50JCDaKjpxsS1p
```

---

## 📄 Pagination

Both servers support **cursor-based pagination**:

| Field | Description |
|:---|:---|
| `cursor` | Marks the next starting position (encoded as string offset) |
| `limit` | Number of items per page (1-100, default 20) |
| `next_cursor` | Cursor for next request (null if on last page) |
| `has_more` | Boolean indicating more records available |
| `total_count` | Total number of records across all pages |

---

## 📊 Request Logging & Correlation

Every tool call is logged with:

- **request_id**: Unique UUID for correlating cross-server calls
- **server_name**: Which server handled the request (job_server / call_log_server)
- **tool_name**: Name of the tool executed
- **args**: Tool arguments (sensitive fields redacted)
- **latency_ms**: Execution time in milliseconds
- **response_size_bytes**: Response payload size
- **status**: success / error

### Sensitive Field Redaction

Fields containing `token`, `auth`, `password`, `secret`, `key`, or `credential` are automatically redacted as `***REDACTED***` in logs.

---

# 🚀 Clone and Run
 
## 📋 Prerequisites
 
- **Python 3.12+**
- **uv** or **pip**
- **Task 2 Job Server** running on port 3001
- **Google Gemini API key** or Claude API key
## 1️⃣ Clone the Repository
 
```bash
git clone <REPO_URL>
cd task_3
```
 
## 2️⃣ Install Dependencies (if needed)
 
```bash
uv sync
# or
pip install -r requirements.txt
```
 
## 3️⃣ Configure Servers
 
Create a `.env` file:
 
```bash
# Call Log Server (port 3000)
TRANSPORT_TYPE_CALL_LOG_SERVER=HTTP
TRANSPORT_PORT_CALL_LOG_SERVER=3000
AUTH_TOKEN=Bearer dddgN6MH20Kx9fjJ5W50JCDaKjpxsS1p
 
# Agent (LLM)
GOOGLE_API_KEY=your-api-key-here
 
# (Optional) Custom server URLs
JOB_SERVER_URL=http://localhost:3001/mcp
CALL_LOG_SERVER_URL=http://localhost:3000/mcp
```
 
## 4️⃣ Start Call Log Server
 
```bash
cd call_log_server
export TRANSPORT_TYPE_CALL_LOG_SERVER=HTTP
export TRANSPORT_PORT_CALL_LOG_SERVER=3000
python server.py
```
 
## 5️⃣ Start Agent
 
```bash
cd ../agent
export GOOGLE_API_KEY="your-api-key"
python -m src.tasks_mcp_server.task_3.agent.main
```
 
## 6️⃣ Interact with Agent
 
```
> What failed calls do we have?
> Create a job for the network issue mentioned earlier.
> Generate a statistics report combining both servers.
> List all open jobs and available technicians.
```
---

## 📋 Environment Variables

### Call Log Server

| Variable | Purpose | Example |
|:---|:---|:---|
| `TRANSPORT_TYPE_CALL_LOG_SERVER` | Server transport | `HTTP` / `STDIO` |
| `TRANSPORT_PORT_CALL_LOG_SERVER` | HTTP port | `3000` |
| `AUTH_TOKEN` | STDIO authentication | `Bearer YOUR_TOKEN` |

### Agent

| Variable | Purpose | Example |
|:---|:---|:---|
| `GOOGLE_API_KEY` | Google Gemini API key | `AIzaSyD...` |
| (Optional) `JOB_SERVER_URL` | Job server endpoint | `http://localhost:3001/mcp` |
| (Optional) `CALL_LOG_SERVER_URL` | Call log server endpoint | `http://localhost:3000/mcp` |

---

## 📝 License

No license file is currently included in the repository.

---

<div align="center">

### 🚀 Task 3 — Multi-Server MCP Agent

**Built with Python + LangChain + MCP + Google Gemini**

🔗 Dual Servers · 🤖 LLM Orchestration · 🔄 Workflow Automation · 📊 Cross-Server Analytics

</div>