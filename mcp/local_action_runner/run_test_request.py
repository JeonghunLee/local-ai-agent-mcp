from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_LOG_DIR = "results/log_mcp_server_local"
DEFAULT_TEMPLATE_VERSION = "v0.0.1"


FIELD_PATTERNS = {
    "template_version": re.compile(r"^- Template Version:\s*(.*)$", re.MULTILINE),
    "request_ref": re.compile(r"^- Branch / Tag / Commit:\s*(.*)$", re.MULTILINE),
    "target_runner": re.compile(r"^- Target Runner:\s*(.*)$", re.MULTILINE),
    "mcp_server_mode": re.compile(r"^- MCP Server Mode:\s*(.*)$", re.MULTILINE),
    "test_tool": re.compile(r"^- Test Tool:\s*(.*)$", re.MULTILINE),
    "test_type": re.compile(r"^- Test Type:\s*(.*)$", re.MULTILINE),
    "target_device_image": re.compile(r"^- Target Device / Image:\s*(.*)$", re.MULTILINE),
    "iterations": re.compile(r"^- Iterations:\s*(.*)$", re.MULTILINE),
}

SUPPORTED_TOOLS = ("build_tool", "flash_tool", "log_analyzer")
TOOL_CHECKLIST_PATTERNS = {
    tool_name: re.compile(rf"^- \[x\]\s*`?{re.escape(tool_name)}`?\s*$", re.MULTILINE | re.IGNORECASE)
    for tool_name in SUPPORTED_TOOLS
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a Test Request issue against the local MCP server.")
    parser.add_argument("--issue-number", type=int, required=True)
    parser.add_argument("--issue-title", required=True)
    parser.add_argument("--issue-body")
    parser.add_argument("--issue-body-file")
    parser.add_argument("--expected-runner", required=True)
    args = parser.parse_args()
    if not args.issue_body and not args.issue_body_file:
        parser.error("one of --issue-body or --issue-body-file is required")
    return args


def extract_fields(issue_body: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for key, pattern in FIELD_PATTERNS.items():
        match = pattern.search(issue_body)
        fields[key] = match.group(1).strip() if match else ""
    if not fields["template_version"]:
        fields["template_version"] = DEFAULT_TEMPLATE_VERSION
    return fields


def split_csv(value: str) -> list[str]:
    return [item.strip().lower() for item in value.split(",") if item.strip()]


def normalize_server_mode(value: str) -> str:
    normalized = value.strip().lower()
    if normalized not in {"direct", "runner"}:
        raise ValueError("MCP Server Mode must be recorded as `direct` or `runner`.")
    return normalized


def resolve_server_module(server_mode: str) -> str:
    if server_mode == "direct":
        return "mcp.server_local_direct.server"
    return "mcp.server_local_runner.server"


def resolve_server_name(server_mode: str) -> str:
    if server_mode == "direct":
        return "mcp-server-local-direct"
    return "mcp-server-local-runner"


def resolve_tool(test_tool: str, test_type: str, target_device_image: str) -> tuple[str, dict[str, Any]]:
    normalized_tool = test_tool.strip().lower()
    normalized_type = test_type.strip().lower()

    if normalized_tool in {"build_tool", "build"}:
        return "build_tool", {
            "target": target_device_image or "all",
            "working_dir": ".",
        }
    if normalized_tool in {"flash_tool", "flash"}:
        return "flash_tool", {
            "interface": "openocd",
            "image": target_device_image or "firmware.bin",
        }
    if normalized_tool in {"log_analyzer", "log", "analyzer"}:
        return "log_analyzer", {
            "log_path": target_device_image or f"{DEFAULT_LOG_DIR}/sample.log",
        }

    if normalized_type in {"build", "build_tool"}:
        return "build_tool", {
            "target": target_device_image or "all",
            "working_dir": ".",
        }
    if normalized_type in {"flash", "flash_tool"}:
        return "flash_tool", {
            "interface": "openocd",
            "image": target_device_image or "firmware.bin",
        }
    if normalized_type in {"log", "log_analyzer", "analyzer"}:
        return "log_analyzer", {
            "log_path": target_device_image or f"{DEFAULT_LOG_DIR}/sample.log",
        }
    raise ValueError(
        "Unsupported Test Tool/Test Type. Use one of: build_tool, flash_tool, log_analyzer."
    )


def resolve_selected_tools(issue_body: str, test_tool: str, test_type: str, target_device_image: str) -> list[tuple[str, dict[str, Any]]]:
    selected_tools = [
        tool_name
        for tool_name, pattern in TOOL_CHECKLIST_PATTERNS.items()
        if pattern.search(issue_body)
    ]
    if selected_tools:
        return [
            resolve_tool(tool_name, test_type, target_device_image)
            for tool_name in selected_tools
        ]

    fallback_tool_name, fallback_arguments = resolve_tool(test_tool, test_type, target_device_image)
    return [(fallback_tool_name, fallback_arguments)]


def call_local_mcp(server_mode: str, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    requests = [
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "issue-test-runner", "version": "0.1"},
            },
        },
        {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
        },
    ]
    payload = "\n".join(json.dumps(request) for request in requests) + "\n"
    result = subprocess.run(
        [sys.executable, "-m", resolve_server_module(server_mode)],
        input=payload,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Local MCP server failed with exit code {result.returncode}: {result.stderr.strip()}"
        )

    responses = [
        json.loads(line)
        for line in result.stdout.splitlines()
        if line.strip()
    ]
    call_response = next((item for item in responses if item.get("id") == 3), None)
    if call_response is None:
        raise RuntimeError("Local MCP server did not return a tools/call response.")

    return {
        "responses": responses,
        "stderr": result.stderr,
        "call_response": call_response,
    }


def parse_call_payload(call_response: dict[str, Any]) -> tuple[dict[str, Any] | None, bool]:
    result = call_response.get("result", {})
    content = result.get("content", [])
    text_value = content[0].get("text", "") if content else ""
    try:
        return json.loads(text_value), bool(result.get("isError"))
    except json.JSONDecodeError:
        return {"raw_text": text_value}, bool(result.get("isError"))


def write_result(issue_number: int, payload: dict[str, Any]) -> Path:
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    output_path = results_dir / f"Github-ISSUE-TR-{issue_number}.json"
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path


def append_summary(lines: list[str]) -> None:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY", "")
    if not summary_path:
        return
    summary_file = Path(summary_path)
    summary_file.parent.mkdir(parents=True, exist_ok=True)
    with summary_file.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def resolve_log_paths(tool_name: str) -> dict[str, str]:
    return {
        "log_dir": DEFAULT_LOG_DIR,
        "server_log": f"{DEFAULT_LOG_DIR}/mcp-server-local.log",
        "tool_log": f"{DEFAULT_LOG_DIR}/mcp-server-local-{tool_name}.log",
    }


def summarize_statuses(tool_results: list[dict[str, Any]]) -> str:
    if any(item["status"] == "error" for item in tool_results):
        return "error"
    return "success"


def main() -> int:
    args = parse_args()
    if args.issue_body is not None:
        issue_body = args.issue_body
    else:
        issue_body = Path(args.issue_body_file).read_text(encoding="utf-8")
    fields = extract_fields(issue_body)

    server_mode = normalize_server_mode(fields["mcp_server_mode"])
    requested_runners = split_csv(fields["target_runner"])
    expected_runner = args.expected_runner.strip().lower()
    timestamp = datetime.now(timezone.utc).isoformat()

    if server_mode == "runner" and expected_runner not in requested_runners:
        payload = {
            "issue_number": args.issue_number,
            "issue_title": args.issue_title,
            "timestamp": timestamp,
            "status": "skipped",
            "reason": "target_runner_mismatch",
            "expected_runner": expected_runner,
            "requested_runners": requested_runners,
            "parsed_fields": fields,
        }
        output_path = write_result(args.issue_number, payload)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        append_summary(
            [
                "## Test Request Result",
                f"- Issue: #{args.issue_number}",
                f"- Status: skipped",
                f"- Reason: target runner `{expected_runner}` was not listed in the issue",
                f"- Result File: `{output_path}`",
            ]
        )
        return 0

    try:
        selected_tools = resolve_selected_tools(
            issue_body,
            fields["test_tool"],
            fields["test_type"],
            fields["target_device_image"],
        )
        server_name = resolve_server_name(server_mode)
        executed_tools: list[dict[str, Any]] = []

        for tool_name, tool_arguments in selected_tools:
            mcp_result = call_local_mcp(server_mode, tool_name, tool_arguments)
            tool_payload, is_error = parse_call_payload(mcp_result["call_response"])
            executed_tools.append(
                {
                    "tool_name": tool_name,
                    "tool_arguments": tool_arguments,
                    "log_paths": resolve_log_paths(tool_name),
                    "status": "error" if is_error else "success",
                    "tool_result": tool_payload,
                }
            )

        status = summarize_statuses(executed_tools)
        payload = {
            "issue_number": args.issue_number,
            "issue_title": args.issue_title,
            "timestamp": timestamp,
            "status": status,
            "expected_runner": expected_runner,
            "requested_runners": requested_runners,
            "resolved_server_mode": server_mode,
            "resolved_server_name": server_name,
            "parsed_fields": fields,
            "selected_tools": [item["tool_name"] for item in executed_tools],
            "tool_runs": executed_tools,
        }
        output_path = write_result(args.issue_number, payload)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        summary_tools = ", ".join(payload["selected_tools"]) or "n/a"
        append_summary(
            [
                "## Test Request Result",
                f"- Issue: #{args.issue_number}",
                f"- Status: {payload['status']}",
                f"- MCP Server Mode: `{server_mode}`",
                f"- MCP Server: `{server_name}`",
                f"- Tools: `{summary_tools}`",
                f"- Request Ref: `{fields['request_ref'] or 'n/a'}`",
                f"- Target Runner: `{fields['target_runner'] or 'n/a'}`",
                f"- Result File: `{output_path}`",
            ]
        )
        return 1 if status == "error" else 0
    except Exception as exc:
        payload = {
            "issue_number": args.issue_number,
            "issue_title": args.issue_title,
            "timestamp": timestamp,
            "status": "error",
            "expected_runner": expected_runner,
            "requested_runners": requested_runners,
            "parsed_fields": fields,
            "error": f"{type(exc).__name__}: {exc}",
        }
        output_path = write_result(args.issue_number, payload)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        append_summary(
            [
                "## Test Request Result",
                f"- Issue: #{args.issue_number}",
                f"- Status: error",
                f"- Error: `{type(exc).__name__}: {exc}`",
                f"- Result File: `{output_path}`",
            ]
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
