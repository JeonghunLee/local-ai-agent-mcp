# MCP Runtime

## Overview

로컬 MCP runtime 예제 디렉터리.   
VS Code `.vscode/mcp.json` 등록용 Python stdio server 구성.

## Files

| File | Role |
|------|------|
| `server_local/runtime.py` | 최소 MCP stdio runtime |
| `server_local/toolsets.py` | Local tool handler |
| `server_local/server_local.py` | Local MCP Server entrypoint |

## VS Code Setup

등록 파일:

```json
{
  "servers": {
    "mcp-server-local": {
      "command": "python",
      "args": ["-m", "mcp.server_local.server_local"]
    }
  }
}
```

## Notes

- 현재 구현: stub server
- Local build / flash 실제 실행 미포함
- 목적: VS Code MCP local server 등록, local tool 골격
