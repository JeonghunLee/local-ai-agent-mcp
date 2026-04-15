# OpenClaw — Local AI Agent Orchestration with MCP

OpenClaw은 MCP(Model Context Protocol)를 통해 여러 AI Agent(Codex, Claude, Ollama)를 조율하는 로컬 멀티 Agent 시스템입니다.

## Project Goals

- 작업 유형과 맥락에 따라 최적의 Agent로 라우팅
- MCP Tool을 통해 Agent 간 통신 및 작업 인계
- 가능한 한 로컬에서 실행 (Ollama), 클라우드 Fallback (Claude, Codex)
- 재현성과 분석을 위해 모든 실행 로그 기록

## Structure

```
└── docs/
    ├── architecture/       시스템 설계 및 Agent 토폴로지
    ├── agents/             Agent별 설정 및 Prompt
    ├── mcp/                MCP 서버 설정 및 Tool 정의
    ├── experiments/        테스트 실행 및 Prompt 실험
    └── logs/               구조화된 실행 로그
```

## Quick Start

1. Ollama 설치 (Windows): [docs/experiments/ollama-setup.md](docs/experiments/ollama-setup.md) 참고
2. OpenClaw 설치 (WSL2): [docs/experiments/wsl2-setup.md](docs/experiments/wsl2-setup.md) 참고
3. MCP 서버 시작: [docs/mcp/mcp-server.md](docs/mcp/mcp-server.md) 참고
4. Agent 설정: [docs/agents/](docs/agents/) 참고
5. 실험 실행: [docs/experiments/openclaw-test.md](docs/experiments/openclaw-test.md) 참고

## Documents

### Architecture
- [시스템 설계](docs/architecture/system-design.md) — Agent 토폴로지, 라우팅 로직, MCP 흐름

### Agents
- [Claude](docs/agents/claude.md) — 추론/분석, Anthropic API
- [Codex](docs/agents/codex.md) — 코드 생성, OpenAI API
- [Ollama](docs/agents/ollama.md) — 로컬 추론, API 키 불필요

### MCP
- [MCP 서버](docs/mcp/mcp-server.md) — 서버 설정, Tool 정의, 프로토콜 흐름

### Claude
- [claude.md](claude.md) — Claude 모델 공급자 설정, API 키, 모델 선택

### Context & Skills
- [context.md](context.md) — 컨텍스트 구성 및 메모리 규칙
- [skill/](skill/) — 문서 접근 규칙 및 일반 실행 규칙

### Experiments
- [ollama-setup.md](docs/experiments/ollama-setup.md) — Windows에서 Ollama 설치
- [wsl2-setup.md](docs/experiments/wsl2-setup.md) — WSL2에서 OpenClaw 설치
- [openclaw-test.md](docs/experiments/openclaw-test.md) — Agent 라우팅 검증 테스트

### Logs
- [run-001.md](docs/logs/run-001.md) — 첫 번째 실행 로그

## Status

설치 진행 중 — Ollama (Windows) + OpenClaw (WSL2)
