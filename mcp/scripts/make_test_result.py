from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_TEMPLATE_VERSION = "v0.0.1"
DEFAULT_SERVER_MODE = "runner"
DEFAULT_TARGET_RUNNER = "local-dev"
DEFAULT_RESULTS_DIR = r"actions-runner\_work\local-ai-agent-mcp\local-ai-agent-mcp\results"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a test request issue comment body.")
    parser.add_argument("--issue-body", required=True)
    parser.add_argument("--result-path", required=True)
    parser.add_argument("--output-path", required=True)
    return parser.parse_args()


def extract_field(issue_body: str, label: str) -> str:
    markdown_pattern = re.compile(rf"^- {re.escape(label)}:\s*(.*)$", re.MULTILINE)
    markdown_match = markdown_pattern.search(issue_body)
    if markdown_match:
        return markdown_match.group(1).strip()

    form_pattern = re.compile(
        rf"^###\s+{re.escape(label)}\s*$\n+(.+?)(?=\n###\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    form_match = form_pattern.search(issue_body)
    if not form_match:
        return "n/a"

    value_lines = [line.strip() for line in form_match.group(1).splitlines() if line.strip()]
    if not value_lines:
        return "n/a"

    first_value = value_lines[0]
    if first_value.startswith("- ["):
        return "n/a"
    return first_value


def load_payload(result_path: Path) -> dict[str, Any] | None:
    if not result_path.exists():
        return None
    return json.loads(result_path.read_text(encoding="utf-8"))


def format_inline_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def parse_request_ref(request_ref: str) -> tuple[str, str]:
    value = (request_ref or "").strip()
    if not value or value == "n/a":
        return "n/a", "n/a"

    sha_match = re.fullmatch(r"[0-9a-fA-F]{7,40}", value)
    if sha_match:
        return "n/a", value

    if "@" in value:
        branch, commit = value.split("@", 1)
        return branch.strip() or "n/a", commit.strip() or "n/a"

    return value, "xxxx"


def resolve_server_name(server_mode: str) -> str:
    if (server_mode or "").strip().lower() == "direct":
        return "mcp-server-local-direct"
    return "mcp-server-local-runner"


def resolve_server_log(server_mode: str) -> str:
    prefix = "direct" if (server_mode or "").strip().lower() == "direct" else "runner"
    return f"results/logs/mcp/server_local/{prefix}.log"


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
    parsed = payload.get("test_request_pared_fileds") or payload.get("parsed_fields", {})
    request_ref = parsed.get("request_ref") or "n/a"
    branch = parsed.get("resolved_branch") or "n/a"
    commit = parsed.get("resolved_commit") or "n/a"
    if branch == "n/a" and commit == "n/a":
        branch, commit = parse_request_ref(request_ref)
    server_mode = parsed.get("mcp_server_mode") or DEFAULT_SERVER_MODE
    target_runner = parsed.get("target_runner") or DEFAULT_TARGET_RUNNER
    server_name = resolve_server_name(server_mode)
    server_log = resolve_server_log(server_mode)
    tool_runs = payload.get("tool_runs") or []

    lines = [
        "## TEST Request Result",
        "",
        f"* Template Version: {parsed.get('template_version') or DEFAULT_TEMPLATE_VERSION}",
        f"* Status: {payload.get('status', 'unknown')}",
        "* Github:",
        f"\t* Branch: {branch}",
        f"\t* Commit: {commit}",
    ]

    if payload.get("reason"):
        lines.append(f"* Reason: {payload['reason']}")

    if payload.get("error"):
        lines.append(f"* Error: {payload['error']}")

    lines.extend(
        [
            "",
            "### 1.TEST Envs ",
            "",
            f"* Target Runner : {target_runner}   ",
            "\t* self-hosted-runner \t",
            f"* result_path: {DEFAULT_RESULTS_DIR}",
            f"\t* MCP Server: {server_name} ",
            f"\t* MCP Server Log: {server_log}",
            "",
            "### 2.Tool Results ",
        ]
    )

    if not tool_runs:
        lines.extend(["", "_No tool results found._"])
        return "\n".join(lines)

    for tool_run in tool_runs:
        tool_name = tool_run.get("tool_function", "n/a")
        tool_args = tool_run.get("tool_args", {})
        tool_result = tool_run.get("tool_result")
        tool_log = "n/a"
        if isinstance(tool_result, dict):
            tool_log = tool_result.get("tool_log", "n/a")

        category = tool_run.get("tool_category", "")
        heading = f"{category}_{tool_name}" if category else tool_name
        lines.extend(
            [
                "",
                f"#### {heading}",
                "",
                f"- Tool Args: {format_inline_json(tool_args)}",
                f"- Tool Log: {tool_log}",
            ]
        )

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
