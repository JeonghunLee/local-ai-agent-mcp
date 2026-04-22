# AI Agent with MCP

<br>

* **Purpose**
  AI Agent workflow based on MCP  
  Connect Claude, Codex, Ollama, and GitHub operations through MCP  
  Support Local MCP execution, GitHub Issue based TEST automation, and documentation-first project flow

<br>

* **Links**
  * GIT: https://github.com/JeonghunLee/local-ai-agent-mcp
  * DOCS: [System Design](architecture/system-design.md)
  * DOCS: [Automation Design](architecture/automation-design.md)

<br>

* **Scope**
  * AI Agent usage
  * MCP Tool integration
  * GitHub automation
  * Local TEST execution
  * CI/CD/CT workflow

<br>

!!! success "Summary"
    Multi-agent workflow with MCP, Local MCP execution, GitHub Issue based TEST automation, and documentation-first project structure.

<br>

## Entry Points

| Area | Document |
|------|------|
| Architecture | [System Design](architecture/system-design.md) |
| Automation | [Automation Design](architecture/automation-design.md) |
| MCP | [MCP Gateway](mcp/mcp_gateway.md) |
| Local Tooling | [MCP Server-Local](mcp/mcp_server_local.md) |
| GitHub Integration | [MCP Server-Github](mcp/mcp_server_github.md) |

---

## Document Groups

| Group | Coverage |
|------|------|
| Architecture | system structure, automation, role split |
| Agents | Claude, Codex, Ollama |
| MCP | Gateway, Local MCP Server, GitHub MCP Server |
| Envs | Windows, WSL2, GitHub operation docs |
| Logs | run records |

---

## Reading Order

1. [System Design](architecture/system-design.md)
2. [Automation Design](architecture/automation-design.md)
3. [MCP Gateway](mcp/mcp_gateway.md)
4. [MCP Server-Local](mcp/mcp_server_local.md)
5. [MCP Server-Github](mcp/mcp_server_github.md)
6. Agent documents
7. Environment documents
