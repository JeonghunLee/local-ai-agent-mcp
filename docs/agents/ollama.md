# Agent: Ollama

## Purpose

로컬, 오프라인 AI 추론. API 키 불필요.

## Models

| 모델           | 용도                      | VRAM   |
|---------------|---------------------------|--------|
| `llama3.2`    | 일반 추론                  | 4 GB   |
| `codellama`   | 오프라인 코드 작업          | 4 GB   |
| `mistral`     | 빠른 일반 작업              | 4 GB   |
| `deepseek-r1` | 추론 / 수학                | 8 GB+  |

## When to Use

- 오프라인 또는 클라우드 의존성 없이 실행해야 하는 작업
- 대용량 / 저비용 추론
- 클라우드 모델 전환 전 프로토타이핑
- 개인정보에 민감한 입력

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

## MCP Tool Signature

```
ollama.run(prompt: string, model?: string) → TextResult
```

## Setup

**Windows**

```powershell
# 방법 1: PowerShell 공식 인스톨러 (권장)
irm https://ollama.com/install.ps1 | iex
```

```powershell
# 방법 2: winget
winget install Ollama.Ollama
```

```powershell
# 방법 3: https://ollama.com/download 에서 .exe 직접 다운로드
```

```powershell
# 모델 다운로드
ollama pull llama3.2

# 실행 확인
ollama list
```

**Linux / macOS**
```bash
# Ollama 설치
curl -fsSL https://ollama.com/install.sh | sh

# 모델 다운로드
ollama pull llama3.2

# 실행 확인
ollama list
```

## Notes

- MCP 서버 시작 전에 Ollama가 로컬에서 실행 중이어야 함
- 클라우드 모델보다 응답 품질이 낮음 — 빠른 필터링이나 단순 작업에 사용
- 실시간 출력이 필요하면 stream 모드 활성화
