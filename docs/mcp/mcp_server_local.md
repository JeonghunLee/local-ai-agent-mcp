# Local MCP Server

<br/>

![VS Code Extension -> MCP Servers](../imgs/mcp_server_local_00.png)

## Overview

<br/>

This document describes the Local MCP Server structure used in the local environment and the GitHub Issue based TEST request flow.

Current repository design:

- one shared Local MCP core
- two entrypoints
  - `mcp.server_local_direct.server`
  - `mcp.server_local_runner.server`

Shared runtime and tool definitions are under `mcp/server_local/`.

```text
mcp/
  scripts/
    make_test_result.py
    run_test_request.py
  server_local/
    runtime.py
    toolsets.py
  server_local_direct/
    server.py
  server_local_runner/
    server.py
```

The key difference is the startup path, not the codebase.

| Mode | Start | Main Context |
|------|------|--------------|
| `direct` | started directly by a VS Code MCP client | local development, direct MCP test |
| `runner` | started through the GitHub Actions Issue flow on a self-hosted runner | GitHub Issue based automated test |

!!! note "Local MCP Server Configuration Entry"
    * The AI Agent Local MCP Server is configured in
      `.vscode/mcp.json`.
    * VS Code reads this file and starts the configured
      Python MCP Server process.
    * The current configuration registers only
      `mcp-server-local-direct`.
    * Issue-based Runner and Jenkins CT start their MCP Server
      through the Python Bridge, not `.vscode/mcp.json`.

<br/>

---

## Local MCP Server Configuration

<br/>

`.vscode/mcp.json` is the repository configuration used by VS Code to register and start the Local MCP Server for an AI Agent.

Current configuration:

```json
{
  "servers": {
    "mcp-server-local-direct": {
      "command": "python",
      "args": [
        "-m",
        "mcp.server_local_direct.server"
      ],
      "cwd": "${workspaceFolder}"
    }
  }
}
```

| Field | Current Value | Role |
|------|------|------|
| Server ID | `mcp-server-local-direct` | name exposed to the VS Code MCP Gateway |
| `command` | `python` | starts the Python interpreter |
| `args` | `-m mcp.server_local_direct.server` | starts the Direct MCP entrypoint |
| `cwd` | `${workspaceFolder}` | uses the repository root as the working directory |

```mermaid
flowchart TD
    Agent["AI Agent"]
    Gateway["VS Code MCP Gateway"]
    Config[".vscode/mcp.json"]
    DirectMCP["mcp-server-local-direct"]
    Runtime["Shared MCP Runtime<br/>runtime.py"]
    SharedTools["Shared TEST Tools<br/>toolsets.py"]
    Result["MCP Tool Result"]

    Agent -->|tool request| Gateway
    Config -->|register and start| Gateway
    Gateway --> DirectMCP --> Runtime --> SharedTools --> Result
    Result -->|tool result| Gateway --> Agent

    classDef config fill:#d0ebff,stroke:#1971c2,stroke-width:3px,color:#000;
    classDef sharedTools fill:#fff3bf,stroke:#f08c00,stroke-width:4px,color:#000;
    class Config config;
    class SharedTools sharedTools;
```

!!! tip "Extending the Local MCP Configuration"
    * Add another entry under `servers` when VS Code must
      start an additional MCP Server.
    * Keep the module path in `args` aligned with the intended
      MCP Server entrypoint.
    * Add third-party Shared TEST Tool packages to
      `mcp_requirements.txt` before starting VS Code.

<br/>

---

## Current Flows - direct

<br/>

This path does not require GitHub Actions or a self-hosted runner.

```text
VS Code MCP Gateway
  -> mcp-server-local-direct
  -> local MCP tools
  -> log files + tool result payload
```

Main purpose:

- local development
- direct MCP client test
- manual tool verification

Entrypoint:

- `python -m mcp.server_local_direct.server`

VS Code configuration source:

- `.vscode/mcp.json`

Current server entry:

```json
{
  "servers": {
    "mcp-server-local-direct": {
      "command": "python",
      "args": ["-m", "mcp.server_local_direct.server"],
      "cwd": "${workspaceFolder}"
    }
  }
}
```

<br/>

---

### Flow

<br/>

```mermaid
flowchart TD
    A["VS Code MCP Gateway"] --> B["mcp-server-local-direct"]
    B --> C["Local tools"]
    C --> D["log files + tool result payload"]
```

<br/>

---

## Current Flows - runner

<br/>

This path requires GitHub Actions and a self-hosted runner.

```text
GitHub Issue
  -> GitHub Actions workflow
  -> Python bridge (mcp.scripts.run_test_request)
  -> mcp-server-local-runner
  -> results/logs/mcp/server_local + results/*.json
  -> GitHub Issue comment
```

Current workflow:

- `.github/workflows/test_request_local.yaml`

Current runner requirement:

- `runs-on: [self-hosted, local-dev]`

This means Issue-based test requests work only when a self-hosted runner with the `local-dev` label is online.

Important points:

- `server_local_direct` can run without GitHub Actions
- however, the `Issue -> Action -> result comment` path requires a self-hosted runner because the workflow executes there

<br/>

---

### Flow

<br/>

```mermaid
flowchart TD
    A["GitHub Issue<br/>Test Request"] --> B["GitHub Actions"]
    B --> D["Self-hosted Runner<br/>[self-hosted, local-dev]"]
    D --> E["Python bridge<br/>mcp.scripts.run_test_request"]
    E --> F["mcp-server-local-runner"]
    F --> G["selected tools"]
    G --> I["results/logs/mcp/server_local<br/>results/*.json"]
    I --> C["GitHub MCP Server"]
    C --> H["Comment result on issue"]
```

<br/>

---

## Flow Decision

<br/>

Use `direct` when:

- a VS Code or local client should start the Local MCP Server directly
- GitHub Issue automation is not needed
- the server should be verified quickly

Use the Issue-based runner flow when:

- execution should start from a GitHub TEST Request Issue
- results should remain as artifact, JSON, log, and Issue comment
- routing to a specific self-hosted runner is required

<br/>

---

## Test Request Flow

<br/>

Current automated TEST Request flow:

```text
GitHub Issue
  -> test_request_local.yaml
  -> mcp.scripts.run_test_request
  -> selected local MCP server
  -> selected tools
  -> results JSON + log files
  -> GitHub Issue result comment
```

<br/>

---

### Request Source

<br/>

Issue body format source:

- `.github/ISSUE_TEMPLATE/test_request_direct.yml`
- `.github/ISSUE_TEMPLATE/test_request_runner.yml`

Current template fields:

- `Template Version`
- `Target Runner`
- `Branch / Tag / Commit`
- category checklist
  - `Setup Tools Checklist`
  - `Test Tools Checklist`
  - `Log Tools Checklist`

Reference:

- [GitHub Templates](../envs/github_templates.md)

<br/>

---

### Python Bridge

<br/>

Bridge script:

- `mcp/scripts/run_test_request.py`

Role:

1. parse Issue body
2. validate `MCP Server Mode`
3. validate `Target Runner` when mode is `runner`
4. resolve checked category and tool list
5. start the Local MCP Server subprocess
6. call MCP tools
7. save result JSON
8. provide output for the final Issue comment step

Execution model:

- `run_test_request.py` does not execute tools directly
- `resolve_server_module()` selects the server module from the mode
- `direct` maps to `mcp.server_local_direct.server`
- `runner` maps to `mcp.server_local_runner.server`
- `call_local_mcp()` starts `python -m <server module>` as a subprocess
- JSON-RPC requests are sent over `stdin`
- request order:
  - `initialize`
  - `notifications/initialized`
  - `tools/list`
  - `tools/call`
- `stdout` is parsed to build the result JSON and Issue comment payload

Practical runner flow:

```text
run_test_request.py
  -> start mcp.server_local_runner.server as subprocess
  -> send JSON-RPC request
  -> receive tool execution result
  -> write results/Github-ISSUE-TR-<issue_number>.json
```

```mermaid
flowchart TD
    A["run_test_request.py"] --> B["resolve_server_module()"]
    B --> C["mcp.server_local_runner.server<br/>subprocess"]
    A --> D["build JSON-RPC payload"]
    D --> C
    C --> E["initialize"]
    C --> F["tools/list"]
    C --> G["tools/call"]
    G --> H["tool execution result"]
    H --> I["results/Github-ISSUE-TR-<issue_number>.json"]
    H --> J["GitHub Issue comment payload"]
```

<br/>

---

### Server Resolution

<br/>

Current resolution logic:

- `direct` -> `mcp.server_local_direct.server`
- `runner` -> `mcp.server_local_runner.server`

Current server names:

- `mcp-server-local-direct`
- `mcp-server-local-runner`

<br/>

---

## Tool Execution

<br/>

Current tool set definition:

- `mcp/server_local/toolsets.py`

Current tool catalog structure:

- `setup`
- `test`
- `log`

Example tools:

- `check_version`
- `setup_python`
- `flash_tool`
- `test_ping_00`
- `test_ping_11`
- `test_ping_22`
- `get_serial_log`
- `log_analyzer`
- `log_snapshot`

The TEST Request template is designed so that one Issue selects one category at a time.

The Python bridge runs the tools from the checked category in sequence and stores the combined result in one JSON file.

Status rule:

- `success` if all tools succeed
- `error` if any tool fails

<br/>

---

## Outputs

<br/>

Current output directories:

- `results/logs/mcp/server_local/`
- `results/`

Current runtime log examples:

- `results/logs/mcp/server_local/runner.log`
- `results/logs/mcp/server_local/runner-check_version.log`
- `results/logs/mcp/server_local/runner-flash_tool.log`
- `results/logs/mcp/server_local/runner-log_analyzer.log`

Current Issue result JSON:

- `results/Github-ISSUE-TR-<issue_number>.json`

Current result JSON fields:

- request metadata
- template version
- resolved MCP server
- selected tools
- per-tool execution result
- per-tool log path

The workflow uploads this file as an artifact and then formats it into an Issue comment.

<br/>

---

## Current Limitations

<br/>

The current implementation is still closer to a test-focused local harness.

- some tools are stubs
- log file naming is tool-name based, not timestamp based
- Issue comment formatting is handled by the workflow script
- Issue-based flow depends on self-hosted runner availability

Current position:

- practical Local MCP Server base
- GitHub Issue based test harness
- expandable to real build, flash, and log analysis behavior

<br/>

---

## Related Files

<br/>

- [MCP Gateway](mcp_gateway.md)
- [MCP Server-GitHub](mcp_server_github.md)
- [GitHub Templates](../envs/github_templates.md)
- [GitHub Self Hosted Runner](../envs/github_self_hosted_runner.md)
- `.github/ISSUE_TEMPLATE/test_request_direct.yml`
- `.github/ISSUE_TEMPLATE/test_request_runner.yml`

<br/>

---
