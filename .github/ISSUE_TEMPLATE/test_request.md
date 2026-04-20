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
[TEST] [<mcp mode>] <YYYY-MM-DD HH:MM> <summary>
[TEST] [<mcp mode>] [<target runner>] <YYYY-MM-DD HH:MM> <summary>
```

Examples:

```text
[TEST] [direct] 2026-04-20 16:30 build_tool smoke
[TEST] [runner] [local-dev] 2026-04-20 16:35 build_tool smoke 
```

## Summary
Describe the test request in one or two sentences.

## Checklist
- [ ] I selected `direct` or `runner` in MCP Server Mode with Target Runner
- [ ] I selected the test tool to run
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

## Test Scope
- Test Tool:
- Test Type:
- Target Device / Image:
- Iterations:

## Logs or References
Add links, issue references, artifacts, or related context if available.
