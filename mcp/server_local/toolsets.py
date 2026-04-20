from __future__ import annotations

import logging
import subprocess


LOGGER = logging.getLogger("local_mcp.tools")
DEFAULT_LOG_DIR = "results/log_mcp_server_local"


def build_tool(arguments: dict) -> dict:
    LOGGER.info("tool.call name=build_tool target=%s working_dir=%s", arguments.get("target", "all"), arguments.get("working_dir", "."))
    result = subprocess.run(
        ["ping", "-n", "5", "127.0.0.1"],
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "tool": "build_tool",
        "status": "success" if result.returncode == 0 else "error",
        "command": "ping -n 5 127.0.0.1",
        "target": arguments.get("target", "all"),
        "working_dir": arguments.get("working_dir", "."),
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def flash_tool(arguments: dict) -> dict:
    LOGGER.info("tool.call name=flash_tool interface=%s image=%s", arguments.get("interface", "openocd"), arguments.get("image", "firmware.bin"))
    return {
        "tool": "flash_tool",
        "status": "success",
        "interface": arguments.get("interface", "openocd"),
        "image": arguments.get("image", "firmware.bin"),
        "message": "Local flash tool stub executed.",
    }


def log_analyzer(arguments: dict) -> dict:
    LOGGER.info("tool.call name=log_analyzer log_path=%s", arguments.get("log_path", f"{DEFAULT_LOG_DIR}/sample.log"))
    return {
        "tool": "log_analyzer",
        "status": "success",
        "log_path": arguments.get("log_path", f"{DEFAULT_LOG_DIR}/sample.log"),
        "summary": "No critical pattern detected in stub analyzer.",
    }


LOCAL_TOOLS = [
    {
        "name": "build_tool",
        "description": "Local build tool stub.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "command": {"type": "string"},
                "target": {"type": "string"},
                "working_dir": {"type": "string"},
            },
        },
    },
    {
        "name": "flash_tool",
        "description": "Local flash tool stub.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "interface": {"type": "string"},
                "image": {"type": "string"},
            },
        },
    },
    {
        "name": "log_analyzer",
        "description": "Local log analyzer stub.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "log_path": {"type": "string"},
            },
        },
    },
]


LOCAL_HANDLERS = {
    "build_tool": build_tool,
    "flash_tool": flash_tool,
    "log_analyzer": log_analyzer,
}
