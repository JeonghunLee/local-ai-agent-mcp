# Agent: Claude

## Purpose

추론, 분석, 장문 컨텍스트 이해, 다단계 계획 수립

## Model

- 제공자: Anthropic
- 모델: `claude-sonnet-4-6` (기본), 복잡한 작업엔 `claude-opus-4-6`
- API: Anthropic Messages API

## When to Use

- 다단계 추론 또는 계획 수립 작업
- 문서 분석 및 요약
- 코드나 아키텍처 결정 설명
- 세밀한 판단이 필요한 작업

## Configuration

```json
{
  "agent": "claude",
  "model": "claude-sonnet-4-6",
  "max_tokens": 4096,
  "system_prompt": "You are a helpful assistant with strong reasoning skills."
}
```

## MCP Tool Signature

```
claude.run(prompt: string, context?: string, thinking?: boolean) → TextResult
```

## Authentication



1. CLI 의 경우, Window의 C:\Users\ahyuo\.claude\.credentials  복사 
2. API 의 경우 


### Method 1: Interactive Login (권장)

```bash
claude auth login
# WSL에서 브라우저가 열리지 않으면 출력된 URL을 Windows 브라우저에서 열기
```

### Method 2: API Key Environment Variable

**WSL / Linux:**
```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.bashrc
source ~/.bashrc
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

### Verify Authentication

```bash
claude auth status
echo $ANTHROPIC_API_KEY   # API Key 설정 여부 확인
claude -p "hello"          # 동작 테스트
```

## Notes

- 깊은 추론이 필요한 작업엔 `claude-opus-4-6` 사용 (비용 높음)
- 복잡한 다단계 문제엔 extended thinking 활성화
- 코드 이해 + 설명이 결합된 작업에 가장 적합한 Agent
