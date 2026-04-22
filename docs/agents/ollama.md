# Agent: Ollama

## Purpose

- local inference
- offline usage
- lightweight analysis
- local model experimentation

---

## When to Use

- offline environment
- low-cost local inference
- local log summary
- simple repeated analysis

---

## Model Options

| Model | Strength | Typical Use |
|------|------|------|
| `llama3.2` | general reasoning | summary, general analysis |
| `mistral` | fast response | quick log check |
| `codellama` | code-oriented | simple code draft |
| `deepseek-r1` | deeper reasoning | more complex local analysis |

---

## Configuration

```json
{
  "agent": "ollama",
  "model": "llama3.2",
  "base_url": "http://localhost:11434",
  "temperature": 0.7,
  "stream": false
}
```

---

## Setup

### Windows

```powershell
irm https://ollama.com/install.ps1 | iex
```

or

```powershell
winget install Ollama.Ollama
```

### Linux / macOS

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Pull Model

```powershell
ollama pull llama3.2
ollama list
```

### Verify API

```powershell
curl http://localhost:11434/api/tags
```

---

## MCP Notes

- local runtime required
- Ollama should be running before MCP server usage
- suitable for local tool support and lightweight analysis

---

## Notes

- strong fit for Local AI role
- better fit for support analysis than complex architecture planning
- WSL2 can access `localhost:11434`
