# Local AI Agent Orchestration with MCP

OpenClaw 기반의 MCP(Model Context Protocol) 사용     
다양한 AI Agent(Codex, Claude, Ollama) 비롯하여 로컬 멀티 Agent 시스템 기능 테스트   

## Project Goals

- OpenClaw의 필요성 확인   
- MCP Tool을 통해 Agent 간 통신 과 AI Agent 의 수 제한 
- 다양한 AI Agent 기반의 TEST 진행    

### Architecture

| 문서 | 설명 |
|------|------|
| [System Design](architecture/system-design.md) | Agent 토폴로지, 라우팅 로직, MCP 흐름 |

### Agents

| 문서 | 설명 |
|------|------|
| [Claude](agents/claude.md) | 추론·분석, Anthropic API |
| [Claude Setup](agents/claude_setup.md) | 인증, Windows 디렉토리 구조 |
| [Claude MCP](agents/claude_mcp.md) | MCP Tool Signature |
| [Codex](agents/codex.md) | 코드 생성, OpenAI API |
| [Ollama](agents/ollama.md) | 로컬 추론, API 키 불필요 |
| [Ollama Setup](agents/ollama_setup.md) | Windows 설치 및 WSL2 연결 |

### MCP

| 문서 | 설명 |
|------|------|
| [MCP Gateway](mcp/mcp_gateway.md) | Tool 라우팅 계층, 다중 MCP Server 연결 |
| [MCP Server-Local](mcp/mcp_server_local.md) | 서버 설정, Tool 정의, Protocol Flow |
| [MCP Server-Github](mcp/mcp_server_github.md) | 서버 설정, Tool 정의, Protocol Flow |

### GitHub

| 문서 | 설명 |
|------|------|
| [GitHub Templates](github/github_templates.md) | Issue · PR · Release · Discussion 템플릿, CT 연동 |

### Environments

| 문서 | 설명 |
|------|------|
| [Windows WSL2 Setup](environments/window_wsl2_setup.md) | WSL2에서 OpenClaw 설치 전체 절차 |
