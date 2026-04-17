# Self-hosted Runner

References:

- GitHub-hosted runners
  https://docs.github.com/ko/actions/reference/runners/github-hosted-runners
- Self-hosted runners
  https://docs.github.com/ko/actions/reference/runners/self-hosted-runners

## Overview

`Target Runner`와 GitHub `self-hosted runner`의 관계
내 PC를 GitHub Actions self-hosted runner로 연결방법.

핵심 개념:
  - `Target Runner`는 TEST 요청을 처리할 실행 주체를 가리키는 논리적 이름        
  - 이 실행 주체는 GitHub Actions의 `self-hosted runner`일 수도 있고, 원격 worker / lab node / 전용 테스트 머신일 수도 있다 
  - 현재 프로젝트에서는 `Target Runner`를 더 넓은 개념으로 사용하되, 가능하면 GitHub runner label과 같은 이름으로 맞춘다 

즉:
  - 문서 설계 관점: `Target Runner` = TEST 요청을 담당할 실행 노드
  - GitHub Actions 관점: `self-hosted runner` = GitHub가 job을 보내는 실행 노드

---

## Quick Start

내 PC를 연결하려면 아래 순서로 진행하면 된다.

1. GitHub 저장소의 `Settings > Actions > Runners`로 이동.
2. `New self-hosted runner`를 runner 등록 명령.
3. 설정 후 Manaul 대로 Download 후 
   - Runner image : Window/Linux/MacOS 선택 
   - Architecture : x86
4. Self-hosted Runner 설정 (`config.cmd`)
      -  Group : default 
5. `runs-on`에 `self-hosted`와 해당 label을 지정.

이 프로젝트 기준으로는 `Target Runner: local-dev`와 runner label `local-dev`를 맞추는 방식을 권장한다.

## Recommended Naming

내 PC를 self-hosted runner로 붙일 때는 runner label을 `Target Runner`와 같은 값으로 맞추는 것이 가장 단순하다.

예:

- 내 PC 이름 역할: `local-dev`
- GitHub runner label: `local-dev`
- TEST 이슈의 `Target Runner`: `local-dev`

이렇게 하면 이슈 운영과 Actions 라우팅이 같은 기준으로 움직인다.

권장 예시:



---

## Connect My PC

### 1. Prepare Runner Directory

이 문서에서는 runner 작업 폴더를 repository 내부에 두는 방식을 기준으로 설명한다.

예:

```powershell
cd D:\works\projects\local-ai-agent-mcp
mkdir action-runner
cd .\action-runner
```

권장 이유:

- 이 프로젝트와 runner 관련 파일 위치를 같이 관리하기 쉽다
- 로컬 문서와 실제 작업 경로가 일치한다
- 테스트용 스크립트나 로그 경로를 repository 기준으로 설명하기 편하다

주의:

- `action-runner` 폴더는 보통 Git으로 추적하지 않는다
- 필요하면 `.gitignore`에 추가해서 관리한다

### 2. Get Registration Commands from GitHub

저장소 기준:

- `Settings`
- `Actions`
- `Runners`
- `New self-hosted runner`


action/runner version 확인  
  https://github.com/actions/runner/releases




### 3. Set Runner Name and Labels

`config.cmd` 실행 중 아래 항목을 묻는다.

- runner group
- runner name
- labels
- service로 설치할지 여부

| Target Runner[] | Meaning |
|---------------|---------|
| `local-dev_00` | 개발자가 직접 관리하는 로컬 실행 환경 |
| `qemu-runner` | 에뮬레이션 기반 테스트 전용 환경 |
| `lab-node-01` | 특정 장비실/하드웨어 노드 |
| `windows-hw-01` | Windows 기반 실장비 테스트 노드 |


* 반드시 관리자 권한 

```Powershell
--------------------------------------------------------------------------------
|        ____ _ _   _   _       _          _        _   _                      |
|       / ___(_) |_| | | |_   _| |__      / \   ___| |_(_) ___  _ __  ___      |
|      | |  _| | __| |_| | | | | '_ \    / _ \ / __| __| |/ _ \| '_ \/ __|     |
|      | |_| | | |_|  _  | |_| | |_) |  / ___ \ (__| |_| | (_) | | | \__ \     |
|       \____|_|\__|_| |_|\__,_|_.__/  /_/   \_\___|\__|_|\___/|_| |_|___/     |
|                                                                              |
|                       Self-hosted runner registration                        |
|                                                                              |
--------------------------------------------------------------------------------

# Authentication


√ Connected to GitHub

# Runner Registration

Enter the name of the runner group to add this runner to: [press Enter for Default] 

Enter the name of runner: [press Enter for JHLEE] local-dev_00

This runner will have the following labels: 'self-hosted', 'Windows', 'X64'
Enter any additional labels (ex. label-1,label-2): [press Enter to skip] local-dev

√ Runner successfully added

# Runner settings

Enter name of work folder: [press Enter for _work]

√ Settings Saved.

Would you like to run the runner as service? (Y/N) [press Enter for N]

```




```text
runner name: my-pc
labels: self-hosted, Windows, X64, local-dev
```

핵심은 기본 label 외에 `local-dev` 같은 프로젝트용 label을 추가하는 것이다.

### 4. Choose How to Run It

일회성 확인은 repository 내부의 `action-runner` 폴더에서 콘솔 실행으로 충분하다.

```powershell
.\run.cmd
```

PC를 켤 때마다 자동으로 붙게 하려면 같은 폴더에서 서비스 설치를 해두는 편이 좋다.

```powershell
.\svc install
.\svc start
```

서비스로 실행하면 로그아웃 후에도 runner가 계속 대기할 수 있다.

### 5. Verify Runner Status in GitHub

등록이 끝나면 `Settings > Actions > Runners` 화면에 runner가 `Idle` 또는 `Online` 상태로 보여야 한다.

보이지 않으면 보통 아래를 확인하면 된다.

- 방화벽 또는 프록시 제한
- 토큰 만료 후 등록 실패
- `run.cmd` 또는 서비스가 실제로 실행 중인지
- label이 기대한 값으로 들어갔는지

---

## Workflow Mapping

runner를 붙여도 workflow가 그 runner를 사용하도록 지정하지 않으면 실제 job은 내려오지 않는다.

예를 들어 내 PC label이 `local-dev`라면:

```yaml
jobs:
  test-on-local-dev:
    runs-on: [self-hosted, local-dev]
    steps:
      - uses: actions/checkout@v4
      - name: Show runner
        run: echo "running on self-hosted local-dev"
```

`runs-on: [self-hosted, local-dev]`는 `self-hosted`이면서 `local-dev` label을 가진 runner만 잡겠다는 뜻이다.

---

## Current Repository Status

현재 저장소의 workflow는 `.github/workflows/github_pages.yaml` 하나이며, 이 파일은 `ubuntu-latest`를 사용한다.

즉 지금 상태에서는 내 PC를 self-hosted runner로 등록해도 자동으로 사용되지는 않는다. 실제로 사용하려면:

- 새 workflow를 추가하거나
- 기존 workflow의 `runs-on`을 self-hosted label 기반으로 바꿔야 한다

---

## Issue-Based Flow

```text
GitHub Issue (TEST 요청)
  → Target Runner 확인
  → 해당 Runner / Worker가 요청 처리
  → Local MCP Tool 실행
  → logs + result.json 생성
  → GitHub Issue 댓글로 결과 보고
```

이 구조에서는 `Target Runner`가 단순 메모가 아니라 실제 실행 소유권과 라우팅 기준이 된다.

---

## Mapping Strategy

권장 매핑은 아래와 같다.

- Issue `Target Runner`: `local-dev`
- GitHub Actions self-hosted runner label: `local-dev`

이렇게 맞추면 사람이 이슈를 보고 판단할 때도 쉽고, 나중에 Actions workflow를 붙일 때도 혼동이 적다.

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
- Local MCP Server: 실행 환경에서 tool을 노출하는 인터페이스
- GitHub MCP Server: GitHub Issue/댓글/상태 변경을 다루는 인터페이스

즉 실제 구조는 다음에 가깝다.

```text
GitHub Issue
  → Runner / Worker
  → GitHub MCP Server로 요청 확인
  → Local MCP Server tool 실행
  → 결과 생성
  → GitHub MCP Server로 결과 보고
```

---

## Recommended Position

현재 프로젝트에서는 `Target Runner`를 다음처럼 이해하는 것이 가장 안전하다.

- 지금: self-hosted runner와 유사한 논리적 실행 노드 이름
- 나중: 필요하면 GitHub Actions self-hosted runner label과 1:1 매핑

특히 내 PC를 runner로 연결할 때는 `local-dev` 같은 label 하나를 기준 이름으로 정해 두는 편이 운영상 가장 편하다.

---

## Related

- [github_templates.md](github_templates.md) — Issue / PR / TEST 요청 템플릿
- [mcp_server_local.md](../mcp/mcp_server_local.md) — Local MCP Server와 TEST 요청 흐름
- [mcp_server_github.md](../mcp/mcp_server_github.md) — GitHub MCP Server 역할
