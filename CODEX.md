# Codex Working Guide

## Purpose

이 문서는 이 저장소에서 Codex가 어떻게 작업해야 하는지 정의.
코드 수정, 문서 편집, 환경 처리, 사용자와의 안전한 협업을 위한 가벼운 운영 가이드.

---

## Role

Codex는 주로 다음 작업에 사용한다.

- 코드 변경 구현
- Markdown 문서 수정 및 정리
- 패치 리뷰와 위험 요소 식별
- 워크플로, 설정, 프로젝트 구조 점검 지원

Codex는 긴 계획보다 직접 실행을 우선하되, 파일을 수정하기 전에 현재 작업에 필요한 최소한의 문맥은 먼저 읽어야 한다.

---

## Project Context

- 프로젝트: `local-ai-agent-mcp`
- 주요 주제: MCP 기반 로컬 AI Agent 오케스트레이션
- 주요 영역: `docs/`, `.github/workflows/`, 환경 설정, Agent 문서, MCP 문서

우선 참고할 문서는 다음과 같다.

- `readme.md`
- `docs/architecture/system-design.md`
- `docs/mcp/mcp_server.md`
- `docs/environments/window_wsl2_setup.md`
- `docs/agents/codex.md`

Codex는 전체 `docs/` 트리를 한꺼번에 읽지 말고, 현재 작업과 관련된 파일만 선택적으로 읽어야 한다.

---

## Working Rules

### Environment

- 현재 기본 셸은 Windows의 PowerShell이다.
- 명령어 작성 시 Windows와 WSL2의 차이를 반드시 구분한다.
- 패키지 설치는 사용자 확인 없이 진행하지 않는다.

### File Edits

- 먼저 읽고, 그다음 수정한다.
- 변경 범위는 작고 명확하게 유지한다.
- 단순 스타일 통일만을 이유로 관련 없는 구간을 다시 쓰지 않는다.
- 사용자가 명시적으로 요청하지 않으면 사용자 변경 사항을 되돌리지 않는다.
- 강한 이유가 없으면 기존 구조와 네이밍을 유지한다.

### Documentation

- 명확한 제목과 간결한 Markdown을 우선한다.
- 아키텍처, 설치, 워크플로 문서는 실용적이고 빠르게 훑어볼 수 있게 작성한다.
- 새 문서를 추가할 때 필요하면 적절한 인덱스 문서에서 링크를 연결한다.
- 명령어, 설정, 예시는 코드 펜스를 사용한다.

### Safety

- 파괴적 작업이나 저장소 전반에 영향을 주는 큰 변경 전에는 먼저 확인한다.
- 명시적 승인 없이 `git push`, 강제 옵션 사용, 위험한 정리 작업을 하지 않는다.
- 시크릿, 토큰, 개인 자격 증명은 절대 하드코딩하지 않는다.

---

## Default Workflow

1. 현재 작업에 필요한 최소 파일 집합을 식별한다.
2. 추측하기 전에 기존 내용을 먼저 읽는다.
3. 요청에 필요한 부분만 수정한다.
4. 가능하면 가벼운 검증을 수행한다.
5. 변경 사항과 남은 공백을 요약한다.

## Preferences For This Repo

- 장황한 설명보다 Markdown의 명확성을 우선한다.
- 예시는 바로 복사해 사용할 수 있게 유지한다.
- 새로운 패턴을 도입하기 전에 기존 저장소 관례를 먼저 따른다.
- 문서를 부수 작업이 아니라 결과물의 일부로 취급한다.

---

## Related Files

- [readme.md](readme.md)
- [docs/architecture/system-design.md](docs/architecture/system-design.md)
- [docs/mcp/mcp_server.md](docs/mcp/mcp_server.md)
- [docs/environments/window_wsl2_setup.md](docs/environments/window_wsl2_setup.md)
- [docs/agents/codex.md](docs/agents/codex.md)
- [CLAUDE.md](CLAUDE.md)
