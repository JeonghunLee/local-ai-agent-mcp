# GitHub Templates

## Overview

이 문서는 현재 저장소에서 사용하는 GitHub 템플릿과  
TEST 요청 흐름에서 각 템플릿이 어떤 역할을 하는지 정리한다.

현재 기준:

- Issue 템플릿은 `.github/ISSUE_TEMPLATE/*`
- Pull Request 템플릿은 `.github/pull_request_template.md`
- TEST 요청은 별도 `Test Request` 이슈 템플릿으로 받는다

이 프로젝트에서는 일반 기능 요청/문서 요청과  
TEST 실행 요청을 분리하는 것이 중요하다.

---

## Template List

| Template | File | Purpose |
|----------|------|---------|
| Bug Report | `.github/ISSUE_TEMPLATE/bug_report.md` | 재현 가능한 버그 보고 |
| Documentation | `.github/ISSUE_TEMPLATE/documentation.md` | 문서 수정/개선 요청 |
| Feature Request | `.github/ISSUE_TEMPLATE/feature_request.md` | 기능 추가/개선 요청 |
| Question | `.github/ISSUE_TEMPLATE/question.md` | 질문 또는 확인 요청 |
| Test Request Direct | `.github/ISSUE_TEMPLATE/test_request_direct.yml` | Jenkins + direct MCP TEST 실행 요청 |
| Test Request Runner | `.github/ISSUE_TEMPLATE/test_request_runner.yml` | self-hosted runner TEST 실행 요청 |
| Pull Request | `.github/pull_request_template.md` | PR 설명, 변경점, 테스트 결과 정리 |

---

## Test Request Template

TEST 실행은 일반 feature/bug issue와 분리해서 받는다.

파일:

- [.github/ISSUE_TEMPLATE/test_request_direct.yml](../../.github/ISSUE_TEMPLATE/test_request_direct.yml)
- [.github/ISSUE_TEMPLATE/test_request_runner.yml](../../.github/ISSUE_TEMPLATE/test_request_runner.yml)

주요 필드:

- `Branch / Tag / Commit`
- `Target Runner`
- `MCP Server Mode`
- `Test Type`
- `Target Device / Image`
- `Iterations`

예시:

```md
## Request Ref
- Template Version: v0.0.1
- Branch / Tag / Commit: 29e157c0
- Target Runner: qemu-runner
- MCP Server Mode: runner

## Test Tool
- [x] `build_tool`
- [ ] `flash_tool`
- [x] `log_analyzer`

## Test Scope
- Test Type: smoke
- Target Device / Image: zephyr.elf
- Iterations: 3
```

One Test Request issue may select multiple tools.

`Template Version` is used to track the request body format.
When the Test Request structure changes, bump this version.

모드 선택 예시:

```md
ex.1
- Target Runner: none
- MCP Server Mode: direct

ex.2
- Target Runner: local-dev
- MCP Server Mode: runner
```

이 템플릿은 다음 흐름을 전제로 한다.

```text
GitHub Issue (TEST 요청)
  → GitHub MCP Server로 이슈 조회
  → Target Runner 확인
  → Local MCP Server Tool 실행
  → logs + result.json 생성
  → GitHub Issue 댓글로 결과 보고
```

---

Recommended title rule:

```text
[TEST] [<mcp mode>] <YYYY-MM-DD HH:MM>
[TEST] [<mcp mode>] [<target runner>] <YYYY-MM-DD HH:MM>
```

Examples:

```text
[TEST] [direct] 2026-04-20 16:30
[TEST] [runner] [local-dev] 2026-04-20 16:35
```

Meaning:

- `mcp mode`: `direct` or `runner`
- `YYYY-MM-DD HH:MM`: local request date/time
- Add `[<target runner>]` when `mcp mode` is `runner`

## Target Runner

`Test Request` 템플릿의 `Target Runner`는 요청을 처리할 실행 노드를 지정한다.

예:

- `local-dev`
- `qemu-runner`
- `lab-node-01`
- `windows-hw-01`

이 값은:

- Local MCP Server를 실행할 환경을 구분하는 데 쓰일 수 있고
- 나중에 GitHub Actions `self-hosted runner` label과 맞출 수도 있다

더 자세한 설명:

- [self-hosted_runner.md](self-hosted_runner.md)

---

## Usage Guidance

### Use Bug Report When

- 이미 발생한 문제를 재현하고 싶을 때
- 증상, 재현 단계, 환경 정보가 핵심일 때

### Use Feature Request When

- 기능 추가나 구조 변경을 제안할 때
- 실행 요청이 아니라 설계/개선 요청일 때

### Use Test Request When

- 특정 ref/commit에 대해 테스트를 실행해달라고 요청할 때
- Runner를 지정해야 할 때
- 결과를 로그/JSON/Issue 댓글로 남기고 싶을 때

즉 TEST는 기능 요청이 아니라 **운영 실행 요청**이므로 별도 템플릿이 더 적합하다.

---

## Pull Request Template

파일:

- [.github/pull_request_template.md](../../.github/pull_request_template.md)

PR 템플릿에는 보통 아래 정보가 포함된다.

- 변경 요약
- 주요 변경점
- 테스트 결과
- 관련 문서 업데이트 여부

TEST 요청과 PR은 역할이 다르다.

- `Test Request`: 실행 요청
- `Pull Request`: 코드 변경 제안

필요하면 TEST Request issue 번호를 PR 본문에 연결할 수 있다.

예:

```md
Related test request: #12
```

---

## Recommended Labeling

TEST 요청 운영 시 함께 쓰기 좋은 label 예시:

- `test-request`
- `test-running`
- `test-done`
- `test-failed`

일반 issue와 TEST issue를 구분하면 라우팅과 추적이 쉬워진다.

---

## Directory Structure

```text
.github/
├── ISSUE_TEMPLATE/
│   ├── bug_report.md
│   ├── documentation.md
│   ├── feature_request.md
│   ├── question.md
│   ├── test_request_direct.yml
│   └── test_request_runner.yml
├── pull_request_template.md
└── workflows/
    └── github_pages.yaml
```

---

## Related

- [self-hosted_runner.md](self-hosted_runner.md) — Target Runner와 self-hosted runner 개념 정리
- [mcp_server_local.md](../mcp/mcp_server_local.md) — Local MCP Server와 TEST 요청 흐름
- [mcp_server_github.md](../mcp/mcp_server_github.md) — GitHub MCP Server 역할
- [mcp_gateway.md](../mcp/mcp_gateway.md) — VS Code MCP Gateway와 다중 MCP Server 연결
