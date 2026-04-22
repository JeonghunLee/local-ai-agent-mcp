# Agent: Claude

## Purpose

- reasoning
- long-context analysis
- document writing
- architecture discussion

---

## When to Use

- structure design
- long document review
- workflow organization
- change plan review before implementation

---

## Model

| Item | Value |
|------|------|
| Provider | Anthropic |
| Default Model | `claude-sonnet-4-6` |
| Higher Tier | `claude-opus-4-6` |
| API | Anthropic Messages API |

---

## Configuration

```json
{
  "agent": "claude",
  "model": "claude-sonnet-4-6",
  "max_tokens": 4096,
  "system_prompt": "You are a helpful assistant with strong reasoning skills."
}
```

---

## Setup

### Rule Files

| Path | Role |
|------|------|
| `claude.md` | project rule file |
| `C:\\Users\\<user>\\.claude\\projects\\d--works-projects-local-ai-agent-mcp\\memory` | project memory |

### Authentication

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

### Verify

```bash
claude auth status
claude -p "hello"
```

---

## MCP Notes

- MCP tool usage available
- strong on long-context reasoning work
- better fit for analysis and design than local execution itself
