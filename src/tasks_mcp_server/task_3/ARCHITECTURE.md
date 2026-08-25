# Demo Architecture

This document shows the complete architecture of the project in a presentation-friendly way.

It includes:

- the Task 2 `job_server` architecture
- the Task 3 `call_log_server` architecture
- the chatbot agent architecture
- the combined data flow between both servers and the agent
- authentication and authorization boundaries

## 1) High-Level System View

```mermaid
flowchart TB
    User[User]
    Agent[Task 3 Agent]

    JobServer[Task 2 job_server MCP Server]
    CallLogServer[Task 3 call_log_server MCP Server]

    JobData[(Jobs / Technicians In-Memory Data)]
    CallData[(Call Logs In-Memory Data)]

    User --> Agent

    Agent --> JobServer
    Agent --> CallLogServer

    JobServer --> JobData
    CallLogServer --> CallData

    JobServer --> Agent
    CallLogServer --> Agent
```

The agent is the orchestration layer. It does not own the domain data itself. Instead, it calls both MCP servers and combines their results into workflows and responses.

## 2) Task 2 Architecture: `job_server`

Task 2 is the authenticated MCP server for jobs and technicians.

```mermaid
flowchart TB
    Client[Client / MCP Host]
    Middleware[AuthenticationMiddleware]
    TokenAuth[Token verification]
    ScopeAuth[Scope authorization]
    Server[FastMCP job_server]

    Tools[Tools]
    Resources[Resources]
    Prompts[Prompts]

    Schemas[Typed schemas]
    Data[(Jobs + Technicians Data)]
    TokenRegistry[(Hardcoded token registry)]

    Client --> Middleware
    Middleware --> TokenAuth
    TokenAuth --> TokenRegistry
    TokenAuth --> ScopeAuth
    ScopeAuth --> Server

    Server --> Tools
    Server --> Resources
    Server --> Prompts

    Tools --> Schemas
    Resources --> Data
    Tools --> Data
    Prompts --> Data
```

### Task 2 request flow

```mermaid
flowchart TB
    Request[Incoming MCP Request]
    Header[Read bearer token]
    Verify[Verify token against registry]
    Expiry[Check token expiry]
    Method[Detect MCP method]
    Tool[Detect tool name]
    Scope[Map method/tool to required scope]
    Allow[Allow request]
    Reject[Reject with structured error]

    Request --> Header --> Verify --> Expiry --> Method --> Tool --> Scope
    Scope -->|valid token + matching scope| Allow
    Scope -->|missing token / invalid token / insufficient scope| Reject
```

### Task 2 auth and authorization boundary

- Authentication confirms the caller is using a valid bearer token.
- Authorization confirms the token has the right scope for the request.
- `read` scope is required for read tools and read-style MCP methods.
- `write` scope is required for write tools.

```mermaid
flowchart LR
    Caller[Caller]
    AuthN[Authentication]
    AuthZ[Authorization]
    Read[Read tools and read methods]
    Write[Write tools]

    Caller --> AuthN
    AuthN --> AuthZ
    AuthZ --> Read
    AuthZ --> Write
```

## 3) Task 3 Architecture: `call_log_server`

Task 3 adds a second MCP server that stores and exposes call-log data.

```mermaid
flowchart TB
    Client[Client / MCP Host]
    Middleware[AuthenticationMiddleware]
    TokenAuth[Token verification]
    ScopeAuth[Scope authorization]
    Server[FastMCP call_log_server]

    Tools[Call-log tools]
    Resources[Resources]
    Prompts[Prompts]

    Schemas[Typed schemas]
    CallData[(Call log data)]
    TokenRegistry[(Hardcoded token registry)]

    Client --> Middleware
    Middleware --> TokenAuth
    TokenAuth --> TokenRegistry
    TokenAuth --> ScopeAuth
    ScopeAuth --> Server

    Server --> Tools
    Server --> Resources
    Server --> Prompts

    Tools --> Schemas
    Resources --> CallData
    Tools --> CallData
    Prompts --> CallData
```

### Task 3 call-log data flow

```mermaid
flowchart TB
    Incoming[Tool call or resource request]
    Auth[Bearer token check]
    Scope[Scope check]
    ToolExec[Execute call-log tool]
    Store[(Call-log in-memory store)]
    Output[Structured MCP response]

    Incoming --> Auth --> Scope --> ToolExec --> Store --> Output
```

The call-log server uses the same general protection model as Task 2:

- bearer token verification
- expiry validation
- scope enforcement
- structured error responses

## 4) Agent Architecture

The agent connects to both MCP servers and exposes their tools to the LLM at runtime.

```mermaid
flowchart TB
    User[User]
    CLI[Chatbot CLI]
    Loop[Agent conversation loop]
    LLM[LLM]
    Router[Tool router]

    JobServer[Task 2 job_server]
    CallLogServer[Task 3 call_log_server]
    WorkflowTools[Workflow tools]

    User --> CLI --> Loop --> LLM
    LLM -->|tool call| Router
    Router --> JobServer
    Router --> CallLogServer
    Router --> WorkflowTools

    JobServer --> Router
    CallLogServer --> Router
    WorkflowTools --> Router
    Router --> Loop
    Loop --> LLM
    LLM --> CLI
```

### Agent data flow

```mermaid
flowchart TB
    Prompt[User prompt]
    Select[LLM selects tool]
    Execute[Agent executes tool]
    Result[Tool result]
    Merge[Agent merges result into chat history]
    Final[Final answer]

    Prompt --> Select --> Execute --> Result --> Merge --> Final
```

The agent logic is:

1. receive user input
2. ask the LLM whether a tool is needed
3. execute the selected MCP tool or workflow tool
4. feed the result back into the conversation
5. continue until the LLM returns a final response

## 5) Combined Data Flow Between Agent and Both Servers

```mermaid
flowchart LR
    U[User]
    A[Agent]
    J[Task 2 job_server]
    C[Task 3 call_log_server]
    JD[(Job / technician data)]
    CD[(Call-log data)]

    U --> A
    A --> J
    A --> C
    J --> JD
    C --> CD
    JD --> J
    CD --> C
    J --> A
    C --> A
    A --> U
```

This is the main integration model:

- Task 2 provides job and technician operations
- Task 3 provides call-log operations
- the agent moves data between them through workflows

## 6) Authentication and Authorization Explanation

### Authentication

Authentication verifies that the caller is known and trusted.

In both servers:

- the client sends a bearer token
- the middleware extracts the token from the request headers
- the token is checked against the hardcoded token registry
- expired or missing tokens are rejected

### Authorization

Authorization verifies that the authenticated token may perform the requested action.

The project uses scope-based authorization:

- `read` scope for read operations
- `write` scope for write operations

The middleware determines the requested MCP method or tool and maps it to the required scope.

### Auth boundary diagram

```mermaid
flowchart TB
    Request[Incoming request]
    Token[Bearer token]
    Registry[(Token registry)]
    ScopeMap[Method/tool to scope map]
    Decision{Authorized?}
    Pass[Allow request]
    Fail[Reject request]

    Request --> Token --> Registry
    Registry --> ScopeMap
    ScopeMap --> Decision
    Decision -->|yes| Pass
    Decision -->|no| Fail
```

### What gets protected

- Task 2 MCP tools
- Task 2 resources and prompts
- Task 3 call-log tools, resources, and prompts
- stdio and HTTP access paths

## 7) Why This Design Works

- The servers stay focused on their own domains.
- The agent can combine capabilities without owning the data.
- Authentication and authorization remain inside the server boundary.
- Structured schemas make responses easier to parse.
- The separation makes the system easier to test, debug, and extend.

## 8) Reference Files

If you want the implementation details behind this diagram, the key files are:

- [`src/tasks_mcp_server/task_2/server.py`](src/tasks_mcp_server/task_2/server.py)
- [`src/tasks_mcp_server/task_2/middleware/middaleware.py`](src/tasks_mcp_server/task_2/middleware/middaleware.py)
- [`src/tasks_mcp_server/task_2/auth/token_auth.py`](src/tasks_mcp_server/task_2/auth/token_auth.py)
- [`src/tasks_mcp_server/task_2/auth/scope_auth.py`](src/tasks_mcp_server/task_2/auth/scope_auth.py)
- [`src/tasks_mcp_server/task_3/call_log_server/server.py`](src/tasks_mcp_server/task_3/call_log_server/server.py)
- [`src/tasks_mcp_server/task_3/call_log_server/middleware/middleware.py`](src/tasks_mcp_server/task_3/call_log_server/middleware/middleware.py)
- [`src/tasks_mcp_server/task_3/agent/main.py`](src/tasks_mcp_server/task_3/agent/main.py)
- [`src/tasks_mcp_server/task_3/agent/mcp_clients.py`](src/tasks_mcp_server/task_3/agent/mcp_clients.py)
