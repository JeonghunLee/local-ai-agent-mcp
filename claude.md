# Claude as OpenClaw Model Provider

## Overview

OpenClaw에서 Claude를 모델 공급자로 사용하는 방법을 설명.
Claude는 추론, 분석, 장문 컨텍스트 처리에 강점이 있어 OpenClaw의 기본 추론 Agent로 적합.

---

## AI Agent Workflow

Agent 역할은 고정되어 있으며 아래 순서로 실행된다.

| 순서 | 작업 유형 | Agent | User 검토 |
|-----|-----------|-------|----------|
| 1 | 구조 설계 / 작업 분해 | Claude (Main) | — |
| 2 | 코드 생성 | Claude (Main) | 1차 승인 / 수정 |
| 3 | 문서 생성 | Claude (Main) | 2차 승인 / 수정 |
| 4 | 코드 리뷰 / 회귀 위험 지적 / patch 초안 | Codex (Sub) | 3차 승인 / 수정 |
| 5 | GitHub PR 요청 | GitHub | — |
| 6 | PR Review | Codex (Sub) + GitHub Users | 4차 승인 / 수정 |
| 7 | TEST 분석 | Codex (Sub) | 5차 승인 / 수정 |
| 8 | TEST 문서 작성 | Codex (Sub) | 6차 승인 / 수정 |

> Remote Agent: Claude (Main) · Codex (Sub) 2개로 제한  
> Ollama (Local): MCP Tool 실행 전담 — 빌드, UART 캡처, QEMU, 레지스터 덤프

---

## Behavior Rules

### Environment

- OS: Windows 11 / Shell: WSL2 (Ubuntu) 기준
- Windows PowerShell은 winget, 환경변수 등 Windows 전용 작업에만 사용
- WSL2 명령어와 PowerShell 명령어를 항상 구분해서 제시한다

### File Operation Rules

- 기존 파일 수정 시: Read → Edit 순서로 진행
- 새 파일 생성 시: Write 사용 (bash heredoc 사용 금지)
- 파일 검색: Glob / Grep 사용 (find, grep 직접 사용 금지)
- 읽지 않은 파일을 Write로 덮어쓰지 않는다

### Docs Rules

- 제목(#, ##, ###): 영어로 유지
- 본문: 한국어
- 서술형 문장 금지 — `실행됩니다` · `실행된다` → `실행`, `저장합니다` → `저장`
- 기술 용어(Agent, Tool, Model, Provider 등)는 번역하지 않고 영어 그대로 사용
- 파일명: 소문자 + 언더스코어 구분 (하이픈 금지)
- 다이어그램은 Mermaid로 작성
- 이미지는 `docs/imgs/`에 보관, 파일명: `소문자_00.png`
- 새 파일 생성 후 상위 인덱스에 링크 추가

### Install Rules

- 설치 작업은 직접 실행하지 않고 사용자에게 요청한다
- 요청 형식: `[환경]에서 아래 명령어를 실행해 주세요` + 코드블록 + `완료되면 알려주세요`
- 설치 완료를 가정하고 다음 단계로 넘어가지 않는다

### Prohibited

- `git push` 등 외부에 영향을 주는 작업은 사용자 확인 후 실행
- `--no-verify`, `--force` 등 안전 장치 우회 금지
- 민감 정보(API 키, 비밀번호) 파일 하드코딩 금지
- 불필요한 주석, docstring, 빈 섹션 추가 금지

---

## Context Rules

### Context Composition Order

```
1. claude.md                        (모든 규칙)
2. 작업 관련 docs/ 문서             (필요한 것만)
3. 현재 대화 히스토리
4. 사용자 입력
```

### Directory Rules

| 디렉토리 | 적용 규칙 |
|---------|----------|
| `docs/` 전체 | Docs Rules 적용 |
| `docs/environments/` | Docs Rules + Install Rules 적용 |
| 설치·실행 작업 | Install Rules 적용 |

### Docs Access Rules

- 작업과 직접 관련된 문서만 읽는다
- 전체 docs/ 를 한꺼번에 읽지 않고 필요한 파일만 읽는다

```
docs/architecture/system-design.md   (구조 파악)
  → docs/agents/<agent>.md           (특정 Agent 작업)
  → docs/environments/<file>.md      (환경 설정)
  → docs/logs/<file>.md              (실행 로그)
```

### Memory Rules

- 세션 간 기억이 필요한 결정사항은 `memory/`에 저장한다
- 임시 작업 상태는 저장하지 않는다
- API 키, 비밀번호 등 민감 정보는 절대 저장하지 않는다

### General Rules

- 이미 확인한 파일은 재읽기 하지 않는다
- 파일 이동/삭제 시 연관 링크를 함께 수정한다
- 실험 수행 후 `docs/logs/`에 결과를 기록한다

---

## Setup

### API Key Setup

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

**WSL2:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.bashrc
```

## Model Selection

| 모델                | 용도                        | 속도  | 비용  |
|--------------------|-----------------------------|------|------|
| `claude-haiku-4-5` | 빠른 응답, 단순 작업          | 빠름 | 낮음 |
| `claude-sonnet-4-6`| 일반 추론, 기본값             | 중간 | 중간 |
| `claude-opus-4-6`  | 복잡한 추론, 장문 분석        | 느림 | 높음 |

## OpenClaw Config Example

```json
{
  "model_provider": "anthropic",
  "model": "claude-sonnet-4-6",
  "max_tokens": 4096,
  "system_prompt": "You are a helpful assistant."
}
```

## Notes

- 로컬 전용이 필요하면 Claude 대신 [Ollama](docs/agents/ollama.md) 사용
- 비용 절감: 단순 작업은 `haiku`, 복잡한 작업만 `opus` 사용

## Related

- [docs/agents/claude.md](docs/agents/claude.md) — MCP Agent로서의 Claude 설정
- [docs/architecture/system-design.md](docs/architecture/system-design.md) — 시스템 구조
