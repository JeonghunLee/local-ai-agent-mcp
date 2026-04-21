from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_TEMPLATE_VERSION = "v0.0.1"
DEFAULT_SERVER_MODE = "runner"
DEFAULT_TARGET_RUNNER = "local-dev"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a test request issue comment body.")
    parser.add_argument("--issue-body", required=True)
    parser.add_argument("--result-path", required=True)
    parser.add_argument("--output-path", required=True)
    return parser.parse_args()


def extract_field(issue_body: str, label: str) -> str:
    pattern = re.compile(rf"^- {re.escape(label)}:\s*(.*)$", re.MULTILINE)
    match = pattern.search(issue_body)
    return match.group(1).strip() if match else "n/a"


def load_payload(result_path: Path) -> dict[str, Any] | None:
    if not result_path.exists():
        return None
    return json.loads(result_path.read_text(encoding="utf-8"))


def render_missing_result(issue_body: str) -> str:
    requested_mode = extract_field(issue_body, "MCP Server Mode")
    requested_runner = extract_field(issue_body, "Target Runner")
    request_ref = extract_field(issue_body, "Branch / Tag / Commit")
    return "\n".join(
        [
            "## Test Request Result",
            "",
            "### 1. TEST Result",
            "- Status: error",
            "- Reason: result file was not created",
            "",
            "### 2. Request Ref",
            f"- Template Version: {extract_field(issue_body, 'Template Version') or DEFAULT_TEMPLATE_VERSION}",
            f"- MCP Server Mode : {requested_mode or DEFAULT_SERVER_MODE}",
            f"- Target Runner   : {requested_runner or DEFAULT_TARGET_RUNNER}",
            f"- Request Ref: {request_ref}",
        ]
    )


def render_payload(payload: dict[str, Any]) -> str:
    parsed = payload.get("parsed_fields", {})
    lines = [
        "## Test Request Result",
        "",
        "### 1. TEST Result",
        f"- Status: {payload.get('status', 'unknown')}",
    ]

    if payload.get("reason"):
        lines.append(f"- Reason: {payload['reason']}")

    if payload.get("error"):
        lines.append(f"- Error: {payload['error']}")

    lines.extend(
        [
            "",
            "### 2. Request Ref",
            f"- Template Version: {parsed.get('template_version') or DEFAULT_TEMPLATE_VERSION}",
            f"- MCP Server Mode (requested): {parsed.get('mcp_server_mode') or 'n/a'}",
            f"- MCP Server (resolved): {payload.get('resolved_server_name') or 'n/a'}",
            f"- Target Runner (requested): {parsed.get('target_runner') or 'n/a'}",
            f"- Target Runner (workflow expected): {payload.get('expected_runner') or 'n/a'}",
            f"- Request Ref: {parsed.get('request_ref') or 'n/a'}",
            "",
            "### 3. Test Scope",
        ]
    )

    if payload.get("selected_tools"):
        lines.append(f"- Selected Tools: {', '.join(payload['selected_tools'])}")
    lines.append(f"- Test Type: {parsed.get('test_type') or 'n/a'}")
    lines.append(f"- Target Device / Image: {parsed.get('target_device_image') or 'n/a'}")
    lines.append(f"- Iterations: {parsed.get('iterations') or 'n/a'}")

    tool_runs = payload.get("tool_runs") or []
    if tool_runs:
        lines.extend(["", "### 4. Logs"])
        for tool_run in tool_runs:
            tool_log = tool_run.get("tool_result", {}).get("tool_log", "n/a")
            lines.append(f"- {tool_run.get('tool_function', 'n/a')}: {tool_log}")

        lines.extend(["", "### 5. Tool Result"])
        for tool_run in tool_runs:
            lines.extend(["", f"#### {tool_run.get('tool_function', 'n/a')}"])
            lines.append(f"- Category: {tool_run.get('tool_category', 'n/a')}")
            if tool_run.get("tool_args") is not None:
                lines.append(f"- Tool Args: {json.dumps(tool_run['tool_args'], ensure_ascii=False)}")
            lines.append(f"- MCP Server Log: {tool_run.get('log_mcp_server', 'n/a')}")

            tool_result = tool_run.get("tool_result")
            if isinstance(tool_result, dict) and tool_result.get("tool_log"):
                lines.append(f"- Tool Log: {tool_result['tool_log']}")
            if tool_result:
                lines.extend(
                    [
                        "",
                        "```json",
                        json.dumps(tool_result, ensure_ascii=False, indent=2),
                        "```",
                    ]
                )

    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    issue_body = args.issue_body
    result_path = Path(args.result_path)
    output_path = Path(args.output_path)

    payload = load_payload(result_path)
    body = render_missing_result(issue_body) if payload is None else render_payload(payload)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(body, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
