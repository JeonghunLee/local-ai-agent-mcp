# Claude as OpenClaw Model Provider

## Overview

OpenClaw에서 Claude를 모델 공급자로 사용하는 방법을 설명합니다.
Claude는 추론, 분석, 장문 컨텍스트 처리에 강점이 있어 OpenClaw의 기본 추론 Agent로 적합합니다.

## Setup

### 1. API Key Setup

Anthropic Console에서 API 키를 발급합니다.
- https://console.anthropic.com/settings/keys

### 2. Select Claude in OpenClaw Onboarding

```bash
openclaw onboard --install-daemon
# 공급자 선택: Anthropic
# API 키 입력
```

### 3. Set via Environment Variable (Optional)

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

**Linux / WSL2:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
# 영구 적용
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.bashrc
```

## Model Selection

| 모델                | 용도                        | 속도  | 비용  |
|--------------------|-----------------------------|------|------|
| `claude-haiku-4-5` | 빠른 응답, 단순 작업          | 빠름 | 낮음 |
| `claude-sonnet-4-6`| 일반 추론, 기본값             | 중간 | 중간 |
| `claude-opus-4-6`  | 복잡한 추론, 장문 분석        | 느림 | 높음 |

## OpenClaw Config Example

```json
{
  "model_provider": "anthropic",
  "model": "claude-sonnet-4-6",
  "max_tokens": 4096,
  "system_prompt": "You are a helpful assistant."
}
```

## Notes

- 로컬 전용이 필요하면 Claude 대신 [Ollama](docs/agents/ollama.md) 사용
- 비용 절감: 단순 작업은 `haiku`, 복잡한 작업만 `opus` 사용
- Agent 설정 상세: [docs/agents/claude.md](docs/agents/claude.md) 참고

## Related

- [docs/agents/claude.md](docs/agents/claude.md) — MCP Agent로서의 Claude 설정
- [context.md](context.md) — 컨텍스트 및 메모리 설정
