# Agent: Codex

## Purpose

코드 생성, 완성, 변환 작업

## Model

- 제공자: OpenAI
- 모델: `gpt-4o` (레거시는 `code-davinci-002`)
- API: OpenAI Completions / Chat API

## When to Use

- 보일러플레이트 또는 스캐폴딩 생성
- 기존 코드 리팩토링
- 함수 시그니처로부터 단위 테스트 작성
- 언어 간 코드 변환

## Configuration

```json
{
  "agent": "codex",
  "model": "gpt-4o",
  "temperature": 0.2,
  "max_tokens": 2048,
  "system_prompt": "You are an expert software engineer. Output only code unless asked to explain."
}
```

## MCP Tool Signature

```
codex.run(prompt: string, language?: string, context_files?: string[]) → CodeResult
```

## Notes

- 결정론적 출력을 위해 temperature를 낮게 유지 (0.1–0.3)
- 정확도 향상을 위해 `context_files`로 관련 파일 컨텍스트 전달
- 추론 없이 순수 코드 출력이 필요할 때 Claude 대신 이 Agent 선택
