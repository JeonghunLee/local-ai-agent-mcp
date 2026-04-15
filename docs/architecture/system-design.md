# System Design

![](../imgs/openclaw_00.png)


## Deployment Diagram

```mermaid
graph TD
    User["사용자 (브라우저)"]

    subgraph Windows11["🖥️ Windows 11 (호스트)"]
        subgraph WSL2["🐧 WSL2 · Ubuntu"]
            OpenClaw["OpenClaw\nOrchestrator\n:18789"]
            MCP["MCP Server\n:3000"]
            OpenClaw -->|MCP Protocol| MCP
        end
        Ollama["Ollama\n:11434\nllama3.2 · codellama"]
        MCP -->|HTTP| Ollama
    end

    subgraph Cloud["☁️ Cloud"]
        Claude["Anthropic\nClaude API"]
        Codex["OpenAI\nCodex API"]
    end

    User -->|HTTP :18789| OpenClaw
    MCP -->|HTTPS| Claude
    MCP -->|HTTPS| Codex
```

---

## Component Details

### 1. User Access
브라우저에서 `http://127.0.0.1:18789` 로 OpenClaw Dashboard에 접속합니다.   
Prompt를 입력하면 Orchestrator가 작업 유형에 맞는 Agent를 선택해 라우팅합니다.

### 2. OpenClaw Orchestrator (WSL2)
- **설치 위치**: WSL2 (Ubuntu)   
- **역할**: Prompt를 받아 적합한 Agent 결정 → MCP 서버로 전달   
- **포트**: `:18789` (Dashboard + Gateway)   
- WSL2에 설치하는 이유: 공식 권장 환경, Linux 네이티브 안정성

### 3. MCP Server (WSL2)
- **설치 위치**: WSL2 (Ubuntu), OpenClaw와 동일 환경   
- **역할**: Agent Adapter 관리, Tool 호출 라우팅   
- **포트**: `:3000`   
- 각 Agent(Claude / Codex / Ollama)에 대한 Adapter를 등록해 통일된 인터페이스 제공

### 4. Ollama (Windows Native)
- **설치 위치**: Windows 11 호스트   
- **역할**: 로컬 LLM 추론, 인터넷 없이 동작   
- **포트**: `:11434`   
- **모델**: `llama3.2` (범용), `codellama` (코드 특화)   
- Windows에 설치하는 이유: GPU 직접 접근으로 추론 성능 최적화   
- WSL2 → Windows 연결: `localhost:11434` 로 투명하게 접근 가능

### 5. Claude API (Cloud)
- **설치 위치**: 없음 — Anthropic 클라우드에서 실행   
- **연결 방식**: `ANTHROPIC_API_KEY` 환경변수   
- **용도**: 추론, 분석, 장문 컨텍스트 처리

### 6. Codex API (Cloud)
- **설치 위치**: 없음 — OpenAI 클라우드에서 실행   
- **연결 방식**: `OPENAI_API_KEY` 환경변수   
- **용도**: 코드 생성, 리팩토링, 언어 변환

---

## Installation Locations

| 컴포넌트     | 설치 위치            | 포트    |
|-------------|---------------------|---------|
| OpenClaw    | WSL2 (Ubuntu)       | :18789  |
| MCP Server  | WSL2 (Ubuntu)       | :3000   |
| Node.js 24  | WSL2 (Ubuntu)       | —       |
| Ollama      | Windows 11 (호스트) | :11434  |
| Claude API  | 클라우드             | —       |
| Codex API   | 클라우드             | —       |

---

## Agent Selection Logic

| 작업 유형        | 우선 Agent | Fallback |
|-----------------|-----------|----------|
| 코드 생성        | Codex     | Claude   |
| 추론 / QA        | Claude    | Ollama   |
| 로컬 / 오프라인  | Ollama    | —        |
| 요약             | Ollama    | Claude   |

---

## Related

- [agents/claude.md](../agents/claude.md) — Claude Agent 설정
- [agents/ollama.md](../agents/ollama.md) — Ollama Agent 설정
- [agents/codex.md](../agents/codex.md) — Codex Agent 설정
- [mcp/mcp_server.md](../mcp/mcp_server.md) — MCP 서버 설정
- [environments/window_wsl2_setup.md](../environments/window_wsl2_setup.md) — WSL2 설치 실험
- [agents/ollama_setup.md](../agents/ollama_setup.md) — Ollama 설치 실험
