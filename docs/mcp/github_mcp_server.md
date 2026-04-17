# GitHub MCP Server

## Overview

GitHub `Repository`, `Pull Request`, `Issue`, `Review`, `Actions` 대상 MCP(Model Context Protocol) `Tool` 제공용 전용 서버.

확인 기준 로그:

```text
2026-04-17 10:33:22.770 [info] Starting server io.github.github/github-mcp-server
2026-04-17 10:33:22.770 [info] Connection state: Starting
2026-04-17 10:33:22.770 [info] Starting server from LocalProcess extension host
2026-04-17 10:33:22.771 [info] Connection state: Running
2026-04-17 10:33:25.037 [info] Discovered resource metadata at https://api.githubcopilot.com/.well-known/oauth-protected-resource/mcp/
2026-04-17 10:33:25.037 [info] Using auth server metadata url: https://github.com/login/oauth
2026-04-17 10:33:25.440 [info] Discovered authorization server metadata at https://github.com/.well-known/oauth-authorization-server/login/oauth
2026-04-17 10:33:33.737 [info] Discovered 44 tools
```

핵심 판단:

- 범용 MCP Server보다 GitHub 전용 MCP Server 성격
- Local 실행 + Remote GitHub 인증/데이터 구조
- `44 tools` 발견 상태

---

## 1. Log Summary

| Log | Meaning |
|------|------|
| `Starting server io.github.github/github-mcp-server` | GitHub MCP Server 시작 |
| `Starting server from LocalProcess extension host` | Local process 기반 실행 |
| `Connection state: Running` | MCP 세션 정상 상태 |
| `Discovered resource metadata at https://api.githubcopilot.com/.../mcp/` | 보호 리소스 메타데이터 탐색 |
| `Using auth server metadata url: https://github.com/login/oauth` | GitHub OAuth 사용 |
| `Discovered authorization server metadata ...` | OAuth 메타데이터 확인 |
| `Discovered 44 tools` | MCP `Tool` 44개 노출 |

### Key Points

- Server process: Local
- Authentication: Remote GitHub OAuth
- Data source: Remote GitHub API
- Runtime shape: `Local Process + Remote GitHub API/OAuth`
- `44 tools`: 시작 시점 discovery 결과

---

## 2. GitHub MCP Server Capabilities

주요 기능군:

- `Repository` 조회 / 검색
- `Pull Request` 조회 / diff / review
- `Issue` 생성 / 수정 / label / assignee
- `Commit` / `Branch` / `File` 조회 및 갱신
- `GitHub Actions` run / job / step / log
- `Review Thread` / `Reaction` / reply / resolve

### Capability Diagram

```mermaid
flowchart LR
    Client["IDE / MCP Client"]
    Server["GitHub MCP Server\nLocal Process"]
    OAuth["GitHub OAuth\nRemote"]
    Meta["Protected Resource Metadata\napi.githubcopilot.com"]
    API["GitHub API\nRepository / PR / Issue / Actions"]

    Client -->|start session| Server
    Server -->|discover metadata| Meta
    Server -->|authenticate| OAuth
    Server -->|read / write tools| API
```

### 2.1 GitHub MCP Server Location (Local / Remote)

| Component | Location | Description |
|------|------|------|
| MCP Server Process | Local | IDE 또는 MCP Client 프로세스 |
| OAuth Server | Remote | `github.com/login/oauth` |
| Protected Resource Metadata | Remote | `api.githubcopilot.com` |
| Data Source | Remote | GitHub `Repository` / `PR` / `Issue` / `Actions` |

### Structure Summary

- Execution: Local
- Auth: Remote
- Data: Remote
- Scope 결정 요소: GitHub API + server implementation

---

## 3. 44 Tools and Their Roles

주의:

- 로그 기준 확인 사실: `Discovered 44 tools`
- 로그 미포함 항목: 개별 `Tool` 이름 전체
- 아래 표: 일반적인 GitHub MCP Server 패턴 기준 역할군 정리
- 실제 목록 확인 수단: MCP Inspector, `tools/list`

### 3.1 Confirmed vs Inferred

| Type | Status | Meaning |
|------|------|------|
| Count | Confirmed | `44 tools` 는 로그로 확인 |
| Exact tool names | Unverified | 개별 Tool 이름은 현재 문서 근거만으로 확인 불가 |
| Exact tool signatures | Unverified | 입력 파라미터, 반환 타입 확인 불가 |
| Role mapping below | Inferred | 일반적인 GitHub MCP Server 패턴 기준 분류 |

### 3.2 Inferred 44-Item Mapping

| No. | Inferred Role Group | Example Tasks | Verification |
|------|------|-----------|------|
| 1 | `Repository Metadata` | 저장소 정보, default branch | Inferred |
| 2 | `Repository Search` | 접근 가능한 저장소 검색 | Inferred |
| 3 | `Branch Search` | branch 검색, 기준 branch 선택 | Inferred |
| 4 | `File Fetch` | 특정 ref 파일 조회 | Inferred |
| 5 | `Blob Fetch` | blob SHA 기반 조회 | Inferred |
| 6 | `Commit Fetch` | 단일 commit 메타데이터, 변경 내용 | Inferred |
| 7 | `Commit Compare` | 두 ref 간 변경 파일, 통계 비교 | Inferred |
| 8 | `Commit Search` | commit 검색 | Inferred |
| 9 | `Commit Status` | combined status, check 결과 | Inferred |
| 10 | `Workflow Run Lookup` | 특정 commit의 Actions run | Inferred |
| 11 | `Workflow Jobs` | run 내 job 목록 | Inferred |
| 12 | `Workflow Steps` | job step 상태 | Inferred |
| 13 | `Workflow Logs` | 실패 job log | Inferred |
| 14 | `PR Metadata` | PR 제목, 상태, base/head branch | Inferred |
| 15 | `PR Diff` | PR diff, patch | Inferred |
| 16 | `PR Patch By File` | 파일 단위 PR patch | Inferred |
| 17 | `PR File List` | 변경 파일 목록 | Inferred |
| 18 | `PR Discussion` | PR comment, review comment, review event | Inferred |
| 19 | `PR Reviews` | review 목록 | Inferred |
| 20 | `PR Review Threads` | inline review thread, resolve 상태 | Inferred |
| 21 | `PR Reactions` | reaction 조회, 추가 | Inferred |
| 22 | `PR Comment Reply` | inline review comment reply | Inferred |
| 23 | `PR Review Submit` | approve, request changes, review 제출 | Inferred |
| 24 | `PR Reviewer Request` | reviewer, team reviewer 요청 | Inferred |
| 25 | `PR Ready/Draft` | Draft, Ready for Review 전환 | Inferred |
| 26 | `PR Update` | 제목, 본문, 상태, base branch 수정 | Inferred |
| 27 | `PR Merge` | merge, squash, rebase | Inferred |
| 28 | `PR Auto Merge` | auto-merge | Inferred |
| 29 | `Issue Fetch` | Issue 본문, 상태, 메타데이터 | Inferred |
| 30 | `Issue Comments` | Issue comment | Inferred |
| 31 | `Issue Create` | Issue 생성 | Inferred |
| 32 | `Issue Update` | 제목, 본문, 상태, milestone 수정 | Inferred |
| 33 | `Issue Labels` | label 추가, 제거 | Inferred |
| 34 | `Issue Assignees` | assignee 추가, 제거 | Inferred |
| 35 | `Issue Lock` | conversation lock, unlock | Inferred |
| 36 | `Issue Comment Update` | top-level comment 수정 | Inferred |
| 37 | `Issue Reactions` | Issue comment reaction | Inferred |
| 38 | `File Create` | 파일 생성 | Inferred |
| 39 | `File Update` | 파일 수정 | Inferred |
| 40 | `File Delete` | 파일 삭제 | Inferred |
| 41 | `Blob Create` | blob 생성 | Inferred |
| 42 | `Tree Create` | Git tree 생성 | Inferred |
| 43 | `Commit Create` | Git commit 생성 | Inferred |
| 44 | `Ref Update` | branch ref 이동, branch 생성 | Inferred |

### Practical Grouping

| Group | Included Capabilities |
|------|-----------|
| Read | `Repository`, `File`, `Commit`, `PR`, `Issue` 조회 |
| Search | `Repository`, `Branch`, code, `PR`, `Issue`, `Commit` 검색 |
| Collaboration | `Review`, comment, reaction, label, assignee |
| CI / Verification | `Actions` run, job, step, log |
| Write | 파일 생성/수정/삭제, branch, commit, merge |

---

## 4. Custom Tool Extensibility

### Conclusion

확장 가능성은 있으나, 현재 문서의 근거만으로는 범위를 단정할 수 없음.

구분 기준:

- GitHub MCP Server 내부 확장
- 별도 Custom MCP Server 추가
- Wrapper / Orchestrator 계층 추가

| Approach | Confidence | Description |
|------|-----------|------|
| Modify GitHub MCP Server itself | Medium | 서버 소스 접근 가능 시 `Tool` 추가 가능성이 높음 |
| Add tools by config only | Low | 설정만으로 임의 `Tool` 추가 가능 여부는 현재 근거 부족 |
| Add a separate Custom MCP Server | High | GitHub 전용 서버와 별도 프로젝트 서버 병행은 일반적으로 현실적 |
| Build a Wrapper Server | High | 여러 GitHub `Tool` 호출을 상위 `Tool`로 추상화하는 방식은 일반적으로 가능 |

### A. Extend the GitHub MCP Server Itself

예시:

- `create_release_summary()`
- `bulk_label_pull_requests()`
- `sync_project_board_item()`

장점:

- GitHub 기능과 직접 통합
- 단일 MCP Server 관점

주의:

- 공식 서버 직접 수정 난이도
- 업스트림 업데이트 시 유지보수 비용

### B. Add a Separate Custom MCP Server

예시:

- `ct_report_publish()`
- `jira_sync()`
- `firmware_test_summary()`
- `local_policy_check()`

장점:

- GitHub MCP Server 비수정
- 프로젝트별 기능 자유도
- 운영 측면 현실성

주의:

- MCP Client 추가 등록 필요
- 역할 경계 문서화 필요

### C. Add a Wrapper / Orchestrator Tool

예시:

- `prepare_release_pr()`
- `review_failed_ci_and_comment()`

조합 예:

1. PR 조회
2. 변경 파일 목록 확인
3. Actions 실패 log 수집
4. comment 작성
5. label 추가

장점:

- 사용자 직접 조합 부담 감소
- workflow 표준화 용이

---

## Recommendation

권장 구성:

- GitHub 데이터 조회/수정: GitHub MCP Server
- 빌드, 테스트, log 분석, 문서 생성: 프로젝트 전용 MCP Server
- 다단계 자동화: Wrapper `Tool` 또는 상위 Orchestrator

---

## Notes

- `44 tools` 수: 서버 버전, 인증 범위, MCP Client 구현 영향
- 실제 개별 목록 필요 시: MCP Inspector 또는 `tools/list` 결과 캡처
- 현재 문서 기준: 확보 로그 + 일반적인 GitHub MCP Server 패턴
- 번호 `1`~`44`: 실제 Tool 이름이 아니라, `44개` 규모를 맞춰 정리한 추정 역할 인덱스
