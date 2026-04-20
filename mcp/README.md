# MCP Runtime

## Overview

로컬 MCP runtime 예제 디렉터리.   
VS Code `.vscode/mcp.json` 등록용 Python stdio server 구성.

## Files

| File | Role |
|------|------|
| `server_local/runtime.py` | 최소 MCP stdio runtime |
| `server_local/toolsets.py` | Local tool handler |
| `server_local_direct/server.py` | Direct Local MCP Server entrypoint |
| `server_local_runner/server.py` | Runner Local MCP Server entrypoint |

## VS Code Setup

등록 파일:

```json
{
  "servers": {
    "mcp-server-local-direct": {
      "command": "python",
      "args": ["-m", "mcp.server_local_direct.server"]
    }
  }
}
```

## Notes

- 공통 코어: `mcp/server_local`
- Direct 실행: `mcp-server-local-direct`
- Runner 실행: `mcp-server-local-runner`
- Local build / flash 실제 실행 미포함
- 목적: VS Code MCP local server 등록, local tool 골격
