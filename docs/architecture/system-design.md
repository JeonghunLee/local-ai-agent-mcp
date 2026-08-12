# System Design

<br/>

## Scope

<br/>

- AI Agent structure
- MCP connection model
- GitHub integration model
- system level role split

<br/>

---

## Document Split

<br/>

This document covers the top-level system structure.

Execution flows and automation details are documented separately:

- [Automation Design](automation-design.md)

<br/>

---

## AI Agents

<br/>

| Agent | Main Role |
|------|------|
| Main AI Agent | code generation, document updates, task structure |
| Sub AI Agent | review, test result analysis, Issue and PR follow-up |
| Local AI Agent | optional local helper, repeated execution support, environment side tasks |

Notes:

- role split first
- deployment shape second
- fixed product mapping not required

Examples:

- Main: Claude or Codex
- Sub: Codex or Claude
- Local: Ollama

<br/>

---

## Remote AI Agents

<br/>

---

### Responsibility

<br/>

- code generation
- document writing
- task split
- review
- test result analysis
- GitHub follow-up

<br/>

---

### Deployment

<br/>

- baseline
  - one Remote AI Agent
- optional extension
  - add Local AI Agent

<br/>

---

### Practical Model

<br/>

- one Remote AI Agent can perform both Main AI and Sub AI roles
- separate Main AI and Sub AI is an operating model, not a hard requirement

<br/>

---

## Local AI Agents

<br/>

---

### Characteristics

<br/>

- optional component
- local execution support
- partial Sub AI replacement possible

<br/>

---

### Examples

<br/>

- Ollama
- MLX
- vLLM

<br/>

---

### Usage

<br/>

- remote API cost reduction
- repeated local test support
- local log and file based analysis support

<br/>

---

## System Diagram

<br/>

```mermaid
flowchart TD
    subgraph UserLayer["User / IDE"]
        User["User"]
        VSCode["VS Code"]
    end

    subgraph AgentLayer["AI Agent / MCP"]
        AIAgent["AI Agent"]
        MCPGateway["MCP Gateway"]
        LocalMCP["Local MCP Server"]
        GitHubMCP["GitHub MCP Server"]
    end

    subgraph GitHubRemote["GitHub Remote"]
        Issue["GitHub Issue"]
        Label{"Issue Label"}
        GitHubActions["GitHub Actions<br/>CI/CD"]
    end

    subgraph Automation["Automation"]
        SelfHosted["Self-hosted Runner"]
        Jenkins["Jenkins"]
    end

    CT["Continuous Testing"]

    User --> VSCode
    VSCode --> AIAgent --> MCPGateway
    MCPGateway --> LocalMCP
    MCPGateway --> GitHubMCP --> Issue

    Issue --> Label
    Label -->|test-request-runner| SelfHosted
    Label -->|test-request-direct| Jenkins
    SelfHosted --> CT
    Jenkins --> CT

    GitHubActions --> SelfHosted
```

The system-level CT flow is selected by the GitHub Issue label:

- `test-request-runner` routes CT to the GitHub self-hosted runner.
- `test-request-direct` routes CT to Jenkins.
- GitHub Actions handles CI/CD jobs through the self-hosted runner.

Workflow scripts, execution steps, and result handling are described in [Automation Design](automation-design.md).

<br/>

---

## AI Agent Working

<br/>

| Step | Work Type | Owner |
|------|------|------|
| 1 | task structure | Main AI |
| 2 | code and document generation | Main AI |
| 3 | review and risk check | Sub AI |
| 4 | local tool execution | Local MCP Server or Local AI |
| 5 | test result analysis | Sub AI |
| 6 | Issue and PR follow-up | GitHub MCP Server or automation |
| 7 | final decision | User |

Notes:

- execution layer and analysis layer split
- one Remote AI Agent can cover step 1, 2, 3, 5, and 6 together

<br/>

---

## Agent Interference

<br/>

- direct overlap minimization
- JSON, log, and comment based handoff
- execution result first
- analysis result second

```text
Local MCP execution
  -> result.json + log
  -> analysis
  -> code or document update
```

<br/>

---

## Design Principles

<br/>

- simple execution path first
- clear split between `direct` and `runner`
- GitHub collaboration and local execution separation
- JSON, log, Markdown comment trace
- Local AI stays optional
- role split does not require fixed process split

<br/>

---

## Related

<br/>

- [Automation Design](automation-design.md)
- [Claude](../agents/claude.md)
- [Codex](../agents/codex.md)
- [Ollama](../agents/ollama.md)
- [MCP Gateway](../mcp/mcp_gateway.md)
- [MCP Server-Local](../mcp/mcp_server_local.md)
- [MCP Server-GitHub](../mcp/mcp_server_github.md)
- [OpenClaw WSL2 Setup](../envs/openclaw_wsl2_setup.md)

<br/>

---
