# Self-hosted Runner

## Overview

이 문서에서는 이 프로젝트에서 말하는 `Target Runner`와  
GitHub `self-hosted runner` 개념의 관계를 정리한다.

핵심 개념:

- `Target Runner`는 TEST 요청을 처리할 실행 주체를 가리키는 논리적 이름이다
- 이 실행 주체는 GitHub Actions의 **self-hosted runner**일 수도 있고,
  그와 유사한 원격 worker / lab node / 전용 테스트 머신일 수도 있다
- 현재 문서에서는 `Target Runner`를 더 넓은 개념으로 사용한다

즉:

- 문서 설계 관점: `Target Runner` = TEST 요청을 담당할 실행 노드
- GitHub Actions 관점: `self-hosted runner` = GitHub가 job을 보내는 실행 노드

둘은 매우 유사하며, 나중에 동일한 이름 체계로 맞출 수 있다.

---

## Why It Matters

Issue 기반 TEST 요청을 사용하면 여러 실행 노드가 동시에 존재할 수 있다.

예:

- `local-dev`
- `windows-hw-01`
- `lab-node-01`
- `qemu-runner`

이 경우 각 요청이 어느 노드에서 처리되어야 하는지 명확해야 한다.  
그래서 TEST 이슈 템플릿에 `Target Runner` 필드를 둔다.

---

## Issue-based Flow

```text
GitHub Issue (TEST 요청)
  → Target Runner 확인
  → 해당 Runner / Worker가 요청 처리
  → Local MCP Tool 실행
  → logs + result.json 생성
  → GitHub Issue 댓글로 결과 보고
```

이 구조에서는 `Target Runner`가 단순 메모가 아니라  
실제 실행 소유권과 라우팅 기준이 된다.

---

## Mapping Strategy

`Target Runner`는 아래처럼 사용할 수 있다.

| Target Runner | Meaning |
|---------------|---------|
| `local-dev` | 개발자가 직접 관리하는 로컬 실행 환경 |
| `qemu-runner` | 에뮬레이션 기반 테스트 전용 환경 |
| `lab-node-01` | 특정 장비실/하드웨어 노드 |
| `windows-hw-01` | Windows 기반 실장비 테스트 노드 |

나중에 GitHub Actions를 연결하면 이 값을 self-hosted runner label과 맞출 수 있다.

예:

- Issue `Target Runner`: `qemu-runner`
- GitHub Actions self-hosted runner label: `qemu-runner`

이렇게 맞추면 Issue 요청과 Actions job 라우팅이 일관된다.

---

## Multiple Runners

`Target Runner`는 단일 값만 사용할 수도 있고, 여러 후보를 둘 수도 있다.

권장 규칙:

- 기본은 단일 runner
- 여러 runner가 필요하면 쉼표 구분 목록 사용
- 의미는 우선 `OR`로 해석

예:

```text
Target Runner: qemu-runner, lab-node-01
```

의미:

- `qemu-runner` 또는 `lab-node-01` 중 하나가 처리 가능
- 먼저 claim한 실행 주체가 처리

---

## Ownership Rules

여러 runner가 동시에 존재할 경우 최소한 아래 규칙이 필요하다.

1. TEST 요청에는 `Target Runner`를 명시한다.
2. 각 runner는 자신이 처리 가능한 요청만 선택한다.
3. 처리 시작 시 assignee 또는 label로 claim 상태를 남긴다.
4. 완료 후 `test-done` 또는 `test-failed` 같은 상태를 기록한다.

추천 label 예시:

- `test-request`
- `test-running`
- `test-done`
- `test-failed`

---

## Relationship with MCP

self-hosted runner 자체가 곧 MCP Server는 아니다.

역할은 다르다.

- Runner / Worker: TEST 요청을 실제로 수행하는 실행 환경
- Local MCP Server: 실행 환경에서 Tool을 노출하는 인터페이스
- GitHub MCP Server: GitHub Issue/댓글/상태 변경을 다루는 인터페이스

즉 실제 구조는 다음에 가깝다.

```text
GitHub Issue
  → Runner / Worker
  → GitHub MCP Server로 요청 확인
  → Local MCP Server Tool 실행
  → 결과 생성
  → GitHub MCP Server로 결과 보고
```

---

## Recommended Position

현재 프로젝트에서는 `Target Runner`를 다음처럼 이해하는 것이 가장 안전하다.

- 지금: self-hosted runner와 유사한 **논리적 실행 노드 이름**
- 나중: 필요하면 GitHub Actions self-hosted runner label과 1:1 매핑

이렇게 두면 문서와 운영 방식이 모두 자연스럽다.

---

## Related

- [github_templates.md](github_templates.md) — Issue / PR / TEST 요청 템플릿
- [mcp_server_local.md](../mcp/mcp_server_local.md) — Local MCP Server와 TEST 요청 흐름
- [mcp_server_github.md](../mcp/mcp_server_github.md) — GitHub MCP Server 역할
