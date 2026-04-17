from __future__ import annotations

import logging


LOGGER = logging.getLogger("local_mcp.tools")


def build_tool(arguments: dict) -> dict:
    LOGGER.info("tool.call name=build_tool")
    return {
        "tool": "build_tool",
        "status": "success",
        "command": arguments.get("command", "make"),
        "target": arguments.get("target", "all"),
        "working_dir": arguments.get("working_dir", "."),
        "message": "Local build tool stub executed.",
    }


def flash_tool(arguments: dict) -> dict:
    LOGGER.info("tool.call name=flash_tool")
    return {
        "tool": "flash_tool",
        "status": "success",
        "interface": arguments.get("interface", "openocd"),
        "image": arguments.get("image", "firmware.bin"),
        "message": "Local flash tool stub executed.",
    }


def log_analyzer(arguments: dict) -> dict:
    LOGGER.info("tool.call name=log_analyzer")
    return {
        "tool": "log_analyzer",
        "status": "success",
        "log_path": arguments.get("log_path", "logs/sample.log"),
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
