from __future__ import annotations

import logging
import subprocess
from collections.abc import Callable
from typing import Any


LOGGER = logging.getLogger("local_mcp.tools")
DEFAULT_LOG_DIR = "results/log_mcp_server_local"

ToolHandler = Callable[[dict[str, Any]], dict[str, Any]]


def check_version(arguments: dict[str, Any]) -> dict[str, Any]:
    command = ["python", "--version"]
    LOGGER.info("tool.call name=check_version")
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "tool": "check_version",
        "status": "success" if result.returncode == 0 else "error",
        "command": " ".join(command),
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def setup_python(arguments: dict[str, Any]) -> dict[str, Any]:
    python_executable = arguments.get("python_executable", "python")
    LOGGER.info("tool.call name=setup_python python=%s", python_executable)
    result = subprocess.run(
        [python_executable, "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "tool": "setup_python",
        "status": "success" if result.returncode == 0 else "error",
        "python_executable": python_executable,
        "message": "Python environment stub verified.",
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def flash_tool(arguments: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info(
        "tool.call name=flash_tool interface=%s image=%s",
        arguments.get("interface", "openocd"),
        arguments.get("image", "firmware.bin"),
    )
    return {
        "tool": "flash_tool",
        "status": "success",
        "interface": arguments.get("interface", "openocd"),
        "image": arguments.get("image", "firmware.bin"),
        "message": "Local flash tool stub executed.",
    }


def build_tool(arguments: dict[str, Any]) -> dict[str, Any]:
    LOGGER.info(
        "tool.call name=build_tool target=%s working_dir=%s",
        arguments.get("target", "all"),
        arguments.get("working_dir", "."),
    )
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


def test_ping_00(arguments: dict[str, Any]) -> dict[str, Any]:
    count = str(arguments.get("count", 2))
    target = arguments.get("target", "127.0.0.1")
    LOGGER.info("tool.call name=test_ping_00 target=%s count=%s", target, count)
    result = subprocess.run(
        ["ping", "-n", count, target],
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "tool": "test_ping_00",
        "status": "success" if result.returncode == 0 else "error",
        "command": f"ping -n {count} {target}",
        "target": target,
        "count": int(count),
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def test_ping_11(arguments: dict[str, Any]) -> dict[str, Any]:
    count = str(arguments.get("count", 4))
    target = arguments.get("target", "127.0.0.1")
    LOGGER.info("tool.call name=test_ping_11 target=%s count=%s", target, count)
    result = subprocess.run(
        ["ping", "-n", count, target],
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "tool": "test_ping_11",
        "status": "success" if result.returncode == 0 else "error",
        "command": f"ping -n {count} {target}",
        "target": target,
        "count": int(count),
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def test_ping_22(arguments: dict[str, Any]) -> dict[str, Any]:
    count = str(arguments.get("count", 6))
    target = arguments.get("target", "127.0.0.1")
    LOGGER.info("tool.call name=test_ping_22 target=%s count=%s", target, count)
    result = subprocess.run(
        ["ping", "-n", count, target],
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "tool": "test_ping_22",
        "status": "success" if result.returncode == 0 else "error",
        "command": f"ping -n {count} {target}",
        "target": target,
        "count": int(count),
        "exit_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def get_serial_log(arguments: dict[str, Any]) -> dict[str, Any]:
    log_path = arguments.get("log_path", f"{DEFAULT_LOG_DIR}/serial.log")
    LOGGER.info("tool.call name=get_serial_log log_path=%s", log_path)
    return {
        "tool": "get_serial_log",
        "status": "success",
        "log_path": log_path,
        "message": "Serial log capture stub executed.",
    }


def log_analyzer(arguments: dict[str, Any]) -> dict[str, Any]:
    log_path = arguments.get("log_path", f"{DEFAULT_LOG_DIR}/sample.log")
    LOGGER.info("tool.call name=log_analyzer log_path=%s", log_path)
    return {
        "tool": "log_analyzer",
        "status": "success",
        "log_path": log_path,
        "summary": "No critical pattern detected in stub analyzer.",
    }


def log_snapshot(arguments: dict[str, Any]) -> dict[str, Any]:
    log_path = arguments.get("log_path", f"{DEFAULT_LOG_DIR}/snapshot.log")
    lines = int(arguments.get("lines", 20))
    LOGGER.info("tool.call name=log_snapshot log_path=%s lines=%s", log_path, lines)
    return {
        "tool": "log_snapshot",
        "status": "success",
        "log_path": log_path,
        "lines": lines,
        "message": "Log snapshot stub collected recent lines.",
    }


TOOL_CATALOG: dict[str, dict[str, Any]] = {
    "check_version": {
        "category": "setup",
        "description": "Check the local Python version.",
        "aliases": ("version",),
        "default_arguments": lambda _target_device_image: {},
        "inputSchema": {
            "type": "object",
            "properties": {},
        },
        "handler": check_version,
    },
    "setup_python": {
        "category": "setup",
        "description": "Local Python setup stub.",
        "aliases": ("python",),
        "default_arguments": lambda _target_device_image: {
            "python_executable": "python",
        },
        "inputSchema": {
            "type": "object",
            "properties": {
                "python_executable": {"type": "string"},
            },
        },
        "handler": setup_python,
    },
    "flash_tool": {
        "category": "setup",
        "description": "Local flash tool stub.",
        "aliases": ("flash",),
        "default_arguments": lambda target_device_image: {
            "interface": "openocd",
            "image": target_device_image or "firmware.bin",
        },
        "inputSchema": {
            "type": "object",
            "properties": {
                "interface": {"type": "string"},
                "image": {"type": "string"},
            },
        },
        "handler": flash_tool,
    },
    "build_tool": {
        "category": "setup",
        "description": "Local build tool stub.",
        "aliases": ("build",),
        "default_arguments": lambda target_device_image: {
            "target": target_device_image or "all",
            "working_dir": ".",
        },
        "inputSchema": {
            "type": "object",
            "properties": {
                "command": {"type": "string"},
                "target": {"type": "string"},
                "working_dir": {"type": "string"},
            },
        },
        "handler": build_tool,
    },
    "test_ping_00": {
        "category": "test",
        "description": "Ping smoke test stub.",
        "aliases": (),
        "default_arguments": lambda _target_device_image: {
            "target": "127.0.0.1",
            "count": 2,
        },
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string"},
                "count": {"type": "integer"},
            },
        },
        "handler": test_ping_00,
    },
    "test_ping_11": {
        "category": "test",
        "description": "Extended ping test stub.",
        "aliases": (),
        "default_arguments": lambda _target_device_image: {
            "target": "127.0.0.1",
            "count": 4,
        },
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string"},
                "count": {"type": "integer"},
            },
        },
        "handler": test_ping_11,
    },
    "test_ping_22": {
        "category": "test",
        "description": "Longer ping verification stub.",
        "aliases": (),
        "default_arguments": lambda _target_device_image: {
            "target": "127.0.0.1",
            "count": 6,
        },
        "inputSchema": {
            "type": "object",
            "properties": {
                "target": {"type": "string"},
                "count": {"type": "integer"},
            },
        },
        "handler": test_ping_22,
    },
    "get_serial_log": {
        "category": "log",
        "description": "Serial log capture stub.",
        "aliases": ("serial_log",),
        "default_arguments": lambda target_device_image: {
            "log_path": target_device_image or f"{DEFAULT_LOG_DIR}/serial.log",
        },
        "inputSchema": {
            "type": "object",
            "properties": {
                "log_path": {"type": "string"},
            },
        },
        "handler": get_serial_log,
    },
    "log_analyzer": {
        "category": "log",
        "description": "Local log analyzer stub.",
        "aliases": ("log", "analyzer"),
        "default_arguments": lambda target_device_image: {
            "log_path": target_device_image or f"{DEFAULT_LOG_DIR}/sample.log",
        },
        "inputSchema": {
            "type": "object",
            "properties": {
                "log_path": {"type": "string"},
            },
        },
        "handler": log_analyzer,
    },
    "log_snapshot": {
        "category": "log",
        "description": "Recent log snapshot stub.",
        "aliases": ("snapshot",),
        "default_arguments": lambda target_device_image: {
            "log_path": target_device_image or f"{DEFAULT_LOG_DIR}/snapshot.log",
            "lines": 20,
        },
        "inputSchema": {
            "type": "object",
            "properties": {
                "log_path": {"type": "string"},
                "lines": {"type": "integer"},
            },
        },
        "handler": log_snapshot,
    },
}


TOOL_CATEGORIES = {
    "setup": tuple(name for name, meta in TOOL_CATALOG.items() if meta["category"] == "setup"),
    "test": tuple(name for name, meta in TOOL_CATALOG.items() if meta["category"] == "test"),
    "log": tuple(name for name, meta in TOOL_CATALOG.items() if meta["category"] == "log"),
}

TOOL_ALIAS_MAP = {
    alias: tool_name
    for tool_name, meta in TOOL_CATALOG.items()
    for alias in (tool_name, *meta.get("aliases", ()))
}

LOCAL_TOOLS = [
    {
        "name": tool_name,
        "description": meta["description"],
        "inputSchema": meta["inputSchema"],
    }
    for tool_name, meta in TOOL_CATALOG.items()
]

LOCAL_HANDLERS: dict[str, ToolHandler] = {
    tool_name: meta["handler"]
    for tool_name, meta in TOOL_CATALOG.items()
}
