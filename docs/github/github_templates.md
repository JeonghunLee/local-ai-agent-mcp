# GitHub Templates

## Overview

GitHub 저장소에서 사용할 수 있는 템플릿 목록.   
모든 템플릿은 `.github/` 디렉터리에 위치한다.

| 템플릿 | 파일 경로 | 용도 |
|--------|----------|------|
| Issue | `.github/ISSUE_TEMPLATE/*.yml` | 버그 리포트, 기능 요청 등 |
| Pull Request | `.github/PULL_REQUEST_TEMPLATE.md` | PR 제출 시 기본 본문 |
| Release Notes | `.github/release.yml` | Release 자동 생성 노트 카테고리 |
| Discussion | `.github/DISCUSSION_TEMPLATE/*.yml` | 토론 카테고리별 양식 |

---

## Issue Template

`.github/ISSUE_TEMPLATE/bug_report.yml`

```yaml
name: Bug Report
description: 버그 및 오류 보고
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        버그를 발견했다면 아래 양식을 작성해 주세요.

  - type: textarea
    id: description
    attributes:
      label: Description
      description: 발생한 문제를 설명하세요.
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: 재현 방법을 순서대로 작성하세요.
      placeholder: |
        1. 
        2. 
        3.
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: 기대했던 동작을 작성하세요.
    validations:
      required: true

  - type: textarea
    id: logs
    attributes:
      label: Logs
      description: 관련 로그가 있으면 첨부하세요.
      render: shell
```

`.github/ISSUE_TEMPLATE/feature_request.yml`

```yaml
name: Feature Request
description: 새 기능 요청
labels: ["enhancement"]
body:
  - type: textarea
    id: problem
    attributes:
      label: Problem
      description: 어떤 문제를 해결하려는지 작성하세요.
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: 원하는 해결 방법을 작성하세요.
    validations:
      required: true
```

---

## Pull Request Template

`.github/PULL_REQUEST_TEMPLATE.md`

```markdown
## Summary

<!-- 변경 사항을 간략히 설명하세요 -->

## Changes

- 

## Test Result

<!-- TEST RESULT 문서 링크 또는 결과 요약 -->

## Checklist

- [ ] 코드 리뷰 완료 (Codex Sub)
- [ ] TEST RESULT 문서 생성 완료
- [ ] 관련 문서 업데이트
```

---

## Release Notes Template

`.github/release.yml`

Release를 생성할 때 PR을 label 기준으로 자동 분류하여 릴리즈 노트를 생성한다.

```yaml
changelog:
  exclude:
    labels:
      - ignore-for-release
  categories:
    - title: Breaking Changes
      labels:
        - breaking-change

    - title: New Features
      labels:
        - enhancement
        - feature

    - title: Bug Fixes
      labels:
        - bug
        - fix

    - title: CT / Test
      labels:
        - test
        - ct

    - title: Documentation
      labels:
        - documentation
        - docs

    - title: Others
      labels:
        - "*"
```

> Release 생성 시 **Generate release notes** 버튼을 누르면 위 카테고리 기준으로 PR 목록이 자동 작성된다.

### Release Trigger → MCP CT 연동

Release가 생성되면 GitHub webhook이 MCP Server로 이벤트를 전송하여 CT를 자동 시작한다.

```yaml
# .github/workflows/ct_trigger.yml
name: CT Trigger on Release

on:
  release:
    types: [published]

jobs:
  trigger-mcp-ct:
    runs-on: ubuntu-latest
    steps:
      - name: Notify MCP Server
        run: |
          curl -X POST http://<MCP_SERVER>:3000/ct/trigger \
            -H "Content-Type: application/json" \
            -d '{
              "event": "release",
              "tag": "${{ github.ref_name }}",
              "release_url": "${{ github.event.release.html_url }}"
            }'
```

---

## Discussion Template

`.github/DISCUSSION_TEMPLATE/general.yml`

```yaml
labels: ["general"]
body:
  - type: textarea
    id: content
    attributes:
      label: Content
    validations:
      required: true
```

---

## Directory Structure

```
.github/
├── ISSUE_TEMPLATE/
│   ├── bug_report.yml
│   └── feature_request.yml
├── DISCUSSION_TEMPLATE/
│   └── general.yml
├── PULL_REQUEST_TEMPLATE.md
├── release.yml
└── workflows/
    └── ct_trigger.yml
```

---

## Related

- [architecture/system-design.md](../architecture/system-design.md) — CT 흐름 및 GitHub Release 트리거
- [mcp/local_mcp_server.md](../mcp/local_mcp_server.md) — MCP Server CT 설정
