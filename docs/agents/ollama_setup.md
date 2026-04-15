# Experiment: Ollama Setup on Windows

## Goal

Windows 11에서 Ollama를 설치하고, WSL2의 OpenClaw와 `localhost:11434`로 연결되는지 검증합니다.

## Environment

| 항목       | 값             |
|-----------|----------------|
| OS        | Windows 11 Pro |
| 설치 방법 | winget         |
| 버전      | 0.20.7         |

## Setup Steps

### Step 1: Install Ollama on Windows

**방법 1 — PowerShell 공식 인스톨러 (권장):**
```powershell
irm https://ollama.com/install.ps1 | iex
```

**방법 2 — winget:**
```powershell
winget install Ollama.Ollama
```

**방법 3 — 직접 다운로드:** https://ollama.com/download 에서 `.exe` 설치

설치 후 시스템 트레이에 Ollama 아이콘이 생기고 자동으로 서비스가 시작됩니다.

### Step 2: Pull Models

```powershell
# 경량 범용 모델 (권장 시작점, 약 2GB)
ollama pull llama3.2

# 코드 특화 모델 (선택)
ollama pull codellama

# 설치된 모델 확인
ollama list
```

### Step 3: Verify API

```powershell
# API 응답 확인
curl http://localhost:11434/api/tags
```

### Step 4: Verify from WSL2

WSL2 안에서도 Windows의 Ollama에 접근 가능합니다.

```bash
# WSL2 터미널에서
curl http://localhost:11434/api/tags
```

> WSL2는 `localhost`를 통해 Windows 호스트 포트에 자동으로 접근됩니다.

## Checklist

- [ ] Ollama 설치 완료 (`irm https://ollama.com/install.ps1 | iex` 또는 winget)
- [ ] 시스템 트레이에 Ollama 아이콘 확인
- [ ] `ollama pull llama3.2` 완료
- [ ] `curl http://localhost:11434/api/tags` → 모델 목록 응답
- [ ] WSL2에서도 동일 주소로 접근 확인

## Result

| 항목                  | 결과    |
|----------------------|---------|
| Windows 설치         | 대기 중 |
| 모델 다운로드         | 대기 중 |
| API 응답             | 대기 중 |
| WSL2 연결            | 대기 중 |

## Notes

- (실행 후 기록)

## Related

- [window_wsl2_setup.md](../environments/window_wsl2_setup.md) — WSL2에서 OpenClaw 설치
- [../agents/ollama.md](../agents/ollama.md) — Ollama 에이전트 설정
