# Agent: Codex

## Purpose

- code generation
- patch writing
- refactoring
- implementation support

---

## When to Use

- code creation
- existing code updates
- boilerplate cleanup
- test code draft

---

## Model

| Item | Value |
|------|------|
| Provider | OpenAI |
| Default Model | `gpt-4o` |
| Role | code-focused generation |
| API | OpenAI API |

---

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

---

## Setup

### Authentication

```powershell
$env:OPENAI_API_KEY = "sk-..."
```

### Verify

```powershell
echo $env:OPENAI_API_KEY
```

---

## MCP Notes

- MCP tool integration available
- better fit for implementation than long-form reasoning
- low temperature recommended for stable output

---

## Notes

- strong fit for code generation
- better fit for patches than long architecture narratives
- useful for review, refactor, and implementation support
