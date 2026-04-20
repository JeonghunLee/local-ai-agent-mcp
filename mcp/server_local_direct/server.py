from mcp.server_local.runtime import MCPServer
from mcp.server_local.toolsets import LOCAL_HANDLERS, LOCAL_TOOLS


if __name__ == "__main__":
    MCPServer(
        name="mcp-server-local-direct",
        version="0.1.0",
        tools=LOCAL_TOOLS,
        handlers=LOCAL_HANDLERS,
    ).run()
