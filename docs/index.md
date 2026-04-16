# OpenClaw — Local AI Agent Orchestration with MCP

OpenClaw은 MCP(Model Context Protocol)를 통해 여러 AI Agent(Codex, Claude, Ollama)를 조율하는 로컬 멀티 Agent 시스템입니다.

## Project Goals

- 작업 유형과 맥락에 따라 최적의 Agent로 라우팅   
- MCP Tool을 통해 Agent 간 통신 및 작업 인계   
- 가능한 한 로컬에서 실행 (Ollama), 클라우드 Fallback (Claude, Codex)   
- 재현성과 분석을 위해 모든 실행 로그 기록

## Quick Start

1. **Ollama 설치 (Windows)** → [agents/ollama_setup.md](agents/ollama_setup.md)   
2. **OpenClaw 설치 (WSL2)** → [environments/window_wsl2_setup.md](environments/window_wsl2_setup.md)   
3. **MCP 서버 시작** → [mcp/mcp_server.md](mcp/mcp_server.md)   
4. **Agent 설정** → [agents/](agents/claude.md)   
5. **실험 실행** → [experiments/openclaw_test.md](experiments/openclaw_test.md)

## Manual

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
| [MCP Server](mcp/mcp_server.md) | 서버 설정, Tool 정의, Protocol Flow |

### GitHub

| 문서 | 설명 |
|------|------|
| [GitHub Templates](github/github_templates.md) | Issue · PR · Release · Discussion 템플릿, CT 연동 |

### Environments

| 문서 | 설명 |
|------|------|
| [Windows WSL2 Setup](environments/window_wsl2_setup.md) | WSL2에서 OpenClaw 설치 전체 절차 |

### Experiments

| 문서 | 설명 |
|------|------|
| [OpenClaw Test](experiments/openclaw_test.md) | Agent 라우팅 검증 테스트 |

### Logs

| 문서 | 설명 |
|------|------|
| [run_001](logs/run_001.md) | 첫 번째 실행 로그 |

## Status

설치 진행 중 — Ollama (Windows) + OpenClaw (WSL2)
