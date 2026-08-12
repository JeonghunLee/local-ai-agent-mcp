# Agent: Claude

<br/>

## Purpose

<br/>

- reasoning
- long-context analysis
- document writing
- architecture discussion

<br/>

---

## When to Use

<br/>

- structure design
- long document review
- workflow organization
- change plan review before implementation

<br/>

---

## Model

<br/>

| Item | Value |
|------|------|
| Provider | Anthropic |
| Default Model | `claude-sonnet-4-6` |
| Higher Tier | `claude-opus-4-6` |
| API | Anthropic Messages API |

<br/>

---

## Configuration

<br/>

```json
{
  "agent": "claude",
  "model": "claude-sonnet-4-6",
  "max_tokens": 4096,
  "system_prompt": "You are a helpful assistant with strong reasoning skills."
}
```

<br/>

---

## Setup

<br/>

---

### Rule Files

<br/>

| Path | Role |
|------|------|
| `claude.md` | project rule file |
| `C:\\Users\\<user>\\.claude\\projects\\d--works-projects-local-ai-agent-mcp\\memory` | project memory |

<br/>

---

### Authentication

<br/>

Method 1:

```bash
claude auth login
```

Method 2:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Method 3:

```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

<br/>

---

### Verify

<br/>

```bash
claude auth status
claude -p "hello"
```

<br/>

---

## MCP Notes

<br/>

- MCP tool usage available
- strong on long-context reasoning work
- better fit for analysis and design than local execution itself

<br/>

---
