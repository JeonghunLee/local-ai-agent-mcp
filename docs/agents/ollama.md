# Agent: Ollama

<br/>

## Purpose

<br/>

- local inference
- offline usage
- lightweight analysis
- local model experimentation

<br/>

---

## When to Use

<br/>

- offline environment
- low-cost local inference
- local log summary
- simple repeated analysis

<br/>

---

## Model Options

<br/>

| Model | Strength | Typical Use |
|------|------|------|
| `llama3.2` | general reasoning | summary, general analysis |
| `mistral` | fast response | quick log check |
| `codellama` | code-oriented | simple code draft |
| `deepseek-r1` | deeper reasoning | more complex local analysis |

<br/>

---

## Configuration

<br/>

```json
{
  "agent": "ollama",
  "model": "llama3.2",
  "base_url": "http://localhost:11434",
  "temperature": 0.7,
  "stream": false
}
```

<br/>

---

## Setup

<br/>

---

### Windows

<br/>

```powershell
irm https://ollama.com/install.ps1 | iex
```

or

```powershell
winget install Ollama.Ollama
```

<br/>

---

### Linux / macOS

<br/>

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

<br/>

---

### Pull Model

<br/>

```powershell
ollama pull llama3.2
ollama list
```

<br/>

---

### Verify API

<br/>

```powershell
curl http://localhost:11434/api/tags
```

<br/>

---

## MCP Notes

<br/>

- local runtime required
- Ollama should be running before MCP server usage
- suitable for local tool support and lightweight analysis

<br/>

---

## Notes

<br/>

- strong fit for Local AI role
- better fit for support analysis than complex architecture planning
- WSL2 can access `localhost:11434`

<br/>

---
