# local-ai-agent-mcp 


* **RAG TEST**          
이전에 MCP Server로 좀 부족할 거 같아, 다양한 부분 테스트  
llamindex/langraph 부터 기타사항      
    https://github.com/JeonghunLee/rag_test

* **Local AI Agent Orchestration with MCP**           
OpenClaw은 MCP(Model Context Protocol)를 통해 여러 AI Agent(Codex, Claude, Ollama, Copliot, Gemini)를 조율.     
**1.로컬 AI Agent 필요성 판단**   
**2.AI Agent 수를 최대한 줄이며, 간단한 연결 방법 모색**           
**3.OpenClaw 필요성 여부 판단**   

* **with OpenClaw 사용**         
    - 나중에 자동채널 비롯하여, E-Mail 부터 Slack을 비롯하여, 관련부분을 연결  
    - Github 의 자동연결    
    - 별도의 Linux 기반 서버로 사용   
    - 각 MCP Server 동작 확인 및 결과 문서 작성  

* **without OpenClaw 사용**         
    - 각 MCP Server 의 세부작업    


## Project Goals

* 개발의 AI Agent와 테스트의 자동화   
    - 작업 유형과 맥락에 따라 최적의 Agent로 라우팅     
    - MCP Tool을 통해 Agent 간 통신 및 작업 인계   
    - 가능한 한 로컬에서 실행 (Ollama), 클라우드 Fallback (Claude, Codex)   
    - 재현성과 분석을 위해 모든 실행 로그 기록     


## Structure

```
└── docs/
    ├── architecture/       시스템 설계 및 Agent 토폴로지
    ├── agents/             Agent별 설정 및 인증
    ├── environments/       환경 설치 가이드 (WSL2 등)
    ├── mcp/                MCP 서버 설정 및 Tool 정의
    ├── experiments/        테스트 실행 및 Prompt 실험
    ├── logs/               구조화된 실행 로그
    └── imgs/               다이어그램 및 스크린샷
```

## Quick Start

1. Ollama 설치 (Windows): [docs/agents/ollama_setup.md](docs/agents/ollama_setup.md)
2. OpenClaw 설치 (WSL2): [docs/environments/window_wsl2_setup.md](docs/environments/window_wsl2_setup.md)
3. MCP Gateway: [docs/mcp/mcp_gateway.md](docs/mcp/mcp_gateway.md)
4. Agent 설정: [docs/agents/](docs/agents/)
5. 실험 실행: [docs/experiments/openclaw_test.md](docs/experiments/openclaw_test.md)

## Documents

### Architecture
- [시스템 설계](docs/architecture/system-design.md) — Agent 토폴로지, 라우팅 로직, MCP 흐름

### Agents
- [Claude](docs/agents/claude.md) — 추론/분석, Anthropic API
- [Claude Setup](docs/agents/claude_setup.md) — 인증, Windows 디렉토리 구조
- [Claude MCP](docs/agents/claude_mcp.md) — MCP Tool Signature
- [Codex](docs/agents/codex.md) — 코드 생성, OpenAI API
- [Ollama](docs/agents/ollama.md) — 로컬 추론, API 키 불필요
- [Ollama Setup](docs/agents/ollama_setup.md) — Windows 설치 및 WSL2 연결

### MCP
- [MCP Gateway](docs/mcp/mcp_gateway.md) — Tool 라우팅 계층, 다중 MCP Server 연결
- [MCP 서버](docs/mcp/mcp_server_local.md) — 서버 설정, Tool 정의, 프로토콜 흐름

### Environments
- [Windows WSL2 Setup](docs/environments/window_wsl2_setup.md) — WSL2에서 OpenClaw 설치

### Experiments
- [openclaw_test.md](docs/experiments/openclaw_test.md) — Agent 라우팅 검증 테스트

### Logs
- [run_001.md](docs/logs/run_001.md) — 첫 번째 실행 로그

## Status

설치완료 — Ollama (Windows) + OpenClaw (WSL2)
기본테스트만 진행   
