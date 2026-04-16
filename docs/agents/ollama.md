# Agent: Ollama

## Purpose

로컬, 오프라인 AI 추론. API 키 불필요.

## Models

| 모델 | 강점 | VRAM | 이 프로젝트 용도 |
|-----|------|------|----------------|
| `llama3.2` | 일반 추론, 요약, 자연어 이해 | 4 GB | 로그 요약, 이상 탐지 |
| `mistral` | 빠른 처리, 지시 따르기 | 4 GB | 대량 로그 분석, 반복 변환 작업 |
| `codellama` | 코드 생성, 코드 설명 | 4 GB | 테스트 초안 생성, 단순 변환 스크립트 |
| `deepseek-r1` | 단계적 추론, 수학 | 8 GB+ | 복잡한 로그 패턴 분석 (고사양 필요) |

### Model Selection Guide

**로그 분석 / 요약**

- 로그 양이 많고 빠른 처리가 우선 → `mistral`
- 맥락 이해·이상 탐지 정확도가 우선 → `llama3.2`
- 패턴이 복잡하고 추론이 필요 → `deepseek-r1` (VRAM 8 GB 이상)

**테스트 자동화**

- 테스트 초안 코드 생성 → `codellama`
- 단순 반복 변환 스크립트 → `mistral`
- 복잡한 테스트 로직 설계 → Claude (Ollama 범위 아님)

**권장 기본 구성**

```
로그 분석: mistral
테스트 초안: codellama
```

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
