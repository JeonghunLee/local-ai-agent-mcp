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

## Notes

- 깊은 추론이 필요한 작업엔 `claude-opus-4-6` 사용 (비용 높음)
- 복잡한 다단계 문제엔 extended thinking 활성화
- 코드 이해 + 설명이 결합된 작업에 가장 적합한 Agent

## Related

- [claude_setup.md](claude_setup.md) — 인증 및 Windows 설정
- [claude_mcp.md](claude_mcp.md) — MCP Tool Signature
