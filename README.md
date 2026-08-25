# Final Project README

## 1) Overview

This repository contains a complete MCP-based field-service project built across three tasks:

- Task 1: a basic MCP server for jobs and technicians
- Task 2: a hardened MCP server with authentication, authorization, pagination, and structured outputs
- Task 3: a multi-server setup with a call-log server and a chatbot agent that uses tools from both servers

The project is designed around the Model Context Protocol so that tools, resources, and prompts can be exposed in a structured way to local clients, remote clients, and an agent workflow.

The main idea of the project is simple:

- jobs represent work that must be completed
- technicians represent people who can do that work
- Task 2 adds production-style safety controls
- Task 3 adds a second server plus an agent that coordinates work across servers

## 2) Explain the Tasks

### Task 1

Task 1 is the foundation of the project. It introduces:

- 8 tools
- 3 resources
- 2 prompts
- in-memory data handling
- support for both `stdio` and Streamable HTTP transport

This task focuses on basic MCP server design and on separating read operations from write operations.

### Task 2

Task 2 hardens the server into a more production-ready implementation. It adds:

- bearer token authentication
- scope-based access control
- cursor-based pagination on all list tools
- structured output schemas on every tool
- strict tool annotations
- dedicated structured error responses

This task is about making the server safer, more predictable, and easier to consume from MCP clients.

### Task 3

Task 3 extends the project into a multi-server architecture. It includes:

- a call-log MCP server
- a chatbot agent that connects to multiple MCP servers
- workflow tools that combine actions across servers
- logging of tool calls, latency, and response size
- an evaluation suite in MCP XML format

This task focuses on orchestration, multi-server tool routing, and agent-driven workflows.

## 3) File Structure

Main project structure:

```text
src/tasks_mcp_server/
├── task_1/
│   ├── core/
│   ├── data/
│   ├── prompts/
│   ├── resources/
│   ├── schemas/
│   ├── services/
│   ├── tools/
│   ├── README.md
│   └── server.py
├── task_2/
│   ├── auth/
│   ├── core/
│   ├── data/
│   ├── middleware/
│   ├── prompts/
│   ├── resources/
│   ├── schemas/
│   ├── services/
│   ├── tools/
│   ├── README.md
│   └── server.py
└── task_3/
    ├── ARCHITECTURE.md
    ├── EVALUATION.xml
    ├── agent/
    │   ├── core/
    │   ├── schemas/
    │   ├── services/
    │   ├── workflows/
    │   ├── README.md
    │   └── main.py
    └── call_log_server/
        ├── auth/
        ├── core/
        ├── data/
        ├── middleware/
        ├── prompts/
        ├── resources/
        ├── schemas/
        ├── services/
        ├── tools/
        ├── README.md
        └── server.py
```

Other important project files:

- `project_requirement.txt` - original task requirements
- `.env.example` - sample environment variables
- `pyproject.toml` - project metadata and dependencies

## 4) How to Clone and Run Both Task 2 and Task 3 Server and Chat Agent

### Prerequisites

- Python 3.12 or newer
- `uv`
- An MCP-compatible client or MCP Inspector

### Clone the repository

```bash
git clone <REPO_URL>
cd Tasks-mcp_server
```

### Install dependencies

```bash
uv sync
```

### Run Task 2 server

Task 2 server entry point:

- `src/tasks_mcp_server/task_2/server.py`

Run in `stdio` mode:

```powershell
$env:TRANSPORT_TYPE="stdio"
$env:AUTH_TOKEN="Bearer YOUR_TOKEN_HERE"
uv run python -m src.tasks_mcp_server.task_2.server
```

Run in HTTP mode:

```powershell
$env:TRANSPORT_TYPE="HTTP"
$env:TRANSPORT_PORT="3000"
uv run python -m src.tasks_mcp_server.task_2.server
```

### Run Task 3 call-log server

Task 3 call-log server entry point:

- `src/tasks_mcp_server/task_3/call_log_server/server.py`

Run in `stdio` mode:

```powershell
$env:TRANSPORT_TYPE="stdio"
$env:AUTH_TOKEN="Bearer YOUR_TOKEN_HERE"
uv run python -m src.tasks_mcp_server.task_3.call_log_server.server
```

Run in HTTP mode:

```powershell
$env:TRANSPORT_TYPE="HTTP"
$env:TRANSPORT_PORT="3001"
uv run python -m src.tasks_mcp_server.task_3.call_log_server.server
```

### Run the chat agent

Agent entry point:

- `src/tasks_mcp_server/task_3/agent/main.py`

Run it from the project root:

```powershell
uv run python -m src.tasks_mcp_server.task_3.agent.main
```

The agent expects the MCP servers to be available and the required model and connection settings to be configured in the environment.

### Suggested run order

1. Start the Task 2 server.
2. Start the Task 3 call-log server.
3. Run the chat agent.
4. Use the agent to exercise workflows that route across both MCP servers.

## 5) Explain the Particular Tasks in Depth

### Task 1 in depth

Task 1 is the base implementation and shows how an MCP server can expose a small business domain cleanly.

Key ideas:

- read tools are separated from write tools
- resources expose current in-memory state
- prompts provide reusable LLM prompt templates
- the same business logic can run in both `stdio` and HTTP modes

The deeper explanation for Task 1 is documented in:

- [`src/tasks_mcp_server/task_1/README.md`](src/tasks_mcp_server/task_1/README.md)

### Task 2 in depth

Task 2 focuses on making the server safer and more reliable.

Important details:

- bearer token authentication is required
- read tools require `scope:read`
- write tools require `scope:write`
- all list tools use cursor-based pagination
- every tool returns structured output
- tool annotations describe read-only, destructive, and idempotent behavior
- errors use a dedicated schema with `error`, `code`, and `suggestion`

This task is also where the repository emphasizes why cursor-based pagination is better than page numbers for changing data sets.

The deeper explanation for Task 2 is documented in:

- [`src/tasks_mcp_server/task_2/README.md`](src/tasks_mcp_server/task_2/README.md)

### Task 3 in depth

Task 3 expands the project into a multi-server system.

Important details:

- the call-log server stores and exposes call log data
- the agent loads tools from multiple MCP servers
- the agent can run workflow tools that combine multiple operations
- every tool call is logged with server name, tool name, arguments, latency, and response size
- if two servers expose tools with related semantics, the agent can combine the results
- the repository includes an architecture diagram and a verified evaluation suite

The deeper explanation for Task 3 is documented in:

- [`src/tasks_mcp_server/task_3/agent/README.md`](src/tasks_mcp_server/task_3/agent/README.md)
- [`src/tasks_mcp_server/task_3/call_log_server/README.md`](src/tasks_mcp_server/task_3/call_log_server/README.md)
- [`src/tasks_mcp_server/task_3/ARCHITECTURE.md`](src/tasks_mcp_server/task_3/ARCHITECTURE.md)
- [`src/tasks_mcp_server/task_3/EVALUATION.xml`](src/tasks_mcp_server/task_3/EVALUATION.xml)

## 6) Author Name

**Mit-007**

## Closing Notes

This final README is meant to serve as the single high-level project summary for the completed repository.

For implementation-level details, the task-specific READMEs remain the best source:

- Task 1: [`src/tasks_mcp_server/task_1/README.md`](src/tasks_mcp_server/task_1/README.md)
- Task 2: [`src/tasks_mcp_server/task_2/README.md`](src/tasks_mcp_server/task_2/README.md)
- Task 3 agent: [`src/tasks_mcp_server/task_3/agent/README.md`](src/tasks_mcp_server/task_3/agent/README.md)
- Task 3 call-log server: [`src/tasks_mcp_server/task_3/call_log_server/README.md`](src/tasks_mcp_server/task_3/call_log_server/README.md)
