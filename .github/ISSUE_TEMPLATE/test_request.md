---
name: Test Request
about: Request a local MCP-driven test run
title: "[TEST] "
labels: test-request
assignees: ""
---

## Recommended Title
Use this format when you create the issue title.

```text
[TEST] [<mcp mode>] <YYYY-MM-DD HH:MM> 
[TEST] [<mcp mode>] [<target runner>] <YYYY-MM-DD HH:MM> 
```

Examples:

```text
[TEST] [direct] 2026-04-20 16:30 
[TEST] [runner] [local-dev] 2026-04-20 16:35 
```

## Summary
Describe the test request in one or two sentences.

## Checklist
- [ ] I selected `direct` or `runner` in MCP Server Mode with Target Runner
- [ ] I recorded the request result

## Request Ref
- Branch / Tag / Commit:
- Target Runner:
- MCP Server Mode:

```md
ex.1 (direct) 
- Target Runner: none
- MCP Server Mode: direct

ex.2 (runner) self-hosted runner 
- Target Runner: local-dev
- MCP Server Mode: runner
```

## Test Tool
- [ ] `build_tool`
- [ ] `flash_tool`
- [ ] `log_analyzer`

Select exactly one tool.

## Test Scope
- Test Type:
- Target Device / Image:
- Iterations:

## Logs or References
Add links, issue references, artifacts, or related context if available.
