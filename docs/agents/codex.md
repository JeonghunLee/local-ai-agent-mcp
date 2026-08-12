# Agent: Codex

<br/>

## Purpose

<br/>

- code generation
- patch writing
- refactoring
- implementation support

<br/>

---

## When to Use

<br/>

- code creation
- existing code updates
- boilerplate cleanup
- test code draft

<br/>

---

## Model

<br/>

| Item | Value |
|------|------|
| Provider | OpenAI |
| Default Model | `gpt-4o` |
| Role | code-focused generation |
| API | OpenAI API |

<br/>

---

## Configuration

<br/>

```json
{
  "agent": "codex",
  "model": "gpt-4o",
  "temperature": 0.2,
  "max_tokens": 2048,
  "system_prompt": "You are an expert software engineer. Output only code unless asked to explain."
}
```

<br/>

---

## Setup

<br/>

---

### Authentication

<br/>

```powershell
$env:OPENAI_API_KEY = "sk-..."
```

<br/>

---

### Verify

<br/>

```powershell
echo $env:OPENAI_API_KEY
```

<br/>

---

## MCP Notes

<br/>

- MCP tool integration available
- better fit for implementation than long-form reasoning
- low temperature recommended for stable output

<br/>

---

## Notes

<br/>

- strong fit for code generation
- better fit for patches than long architecture narratives
- useful for review, refactor, and implementation support

<br/>

---
