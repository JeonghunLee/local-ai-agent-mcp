import json
import logging
import sys
from typing import Any, Callable


JsonDict = dict[str, Any]
ToolHandler = Callable[[JsonDict], JsonDict]


LOGGER = logging.getLogger("local_mcp")
if not LOGGER.handlers:
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("[%(levelname)s] [%(name)s] %(message)s"))
    LOGGER.addHandler(handler)
LOGGER.setLevel(logging.INFO)
LOGGER.propagate = False


class MCPServer:
    def __init__(self, name: str, version: str, tools: list[JsonDict], handlers: dict[str, ToolHandler]):
        self.name = name
        self.version = version
        self.tools = tools
        self.handlers = handlers

    def run(self) -> None:
        self._log_info(f"server.start name={self.name} version={self.version}")
        while True:
            try:
                message = self._read_message()
            except Exception as exc:  # pragma: no cover - defensive fallback
                self._log_info(
                    f"server.read_error name={self.name} error={type(exc).__name__}: {exc}"
                )
                continue
            if message is None:
                self._log_info(f"server.stop name={self.name} reason=stdin_closed")
                return
            self._log_info(
                f"server.recv name={self.name} method={message.get('method')} id={message.get('id')}"
            )
            response = self._handle_message(message)
            if response is not None:
                self._log_info(
                    f"server.send name={self.name} id={response.get('id')} "
                    f"result={'error' if response.get('error') else 'ok'}"
                )
                self._write_message(response)

    def _handle_message(self, message: JsonDict) -> JsonDict | None:
        if not isinstance(message, dict):
            return self._error_response(None, -32600, "Invalid Request")

        method = message.get("method")
        request_id = message.get("id")

        if method == "initialize":
            self._log_info(f"server.initialize name={self.name}")
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": self.name, "version": self.version},
                },
            }

        if method == "notifications/initialized" or method == "initialized":
            return None

        if method == "ping":
            self._log_info(f"server.ping name={self.name}")
            return {"jsonrpc": "2.0", "id": request_id, "result": {}}

        if method == "tools/list":
            self._log_info(f"server.tools_list name={self.name} count={len(self.tools)}")
            return {"jsonrpc": "2.0", "id": request_id, "result": {"tools": self.tools}}

        if method == "tools/call":
            params = message.get("params", {})
            if not isinstance(params, dict):
                return self._error_response(request_id, -32602, "Invalid params")

            tool_name = params.get("name", "")
            arguments = params.get("arguments", {})
            if arguments is None:
                arguments = {}
            if not isinstance(arguments, dict):
                return self._error_response(request_id, -32602, "Invalid params")
            self._log_info(
                f"server.tools_call name={self.name} tool={tool_name} "
                f"arguments={json.dumps(arguments, ensure_ascii=False)}"
            )
            handler = self.handlers.get(tool_name)

            if handler is None:
                self._log_info(f"server.tools_call_unknown name={self.name} tool={tool_name}")
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": f"Unknown tool: {tool_name}"}],
                        "isError": True,
                    },
                }

            try:
                payload = handler(arguments)
                self._log_info(f"server.tools_call_done name={self.name} tool={tool_name}")
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False, indent=2)}],
                        "isError": False,
                    },
                }
            except Exception as exc:  # pragma: no cover - defensive fallback
                self._log_info(
                    f"server.tools_call_error name={self.name} tool={tool_name} "
                    f"error={type(exc).__name__}: {exc}"
                )
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{"type": "text", "text": f"{type(exc).__name__}: {exc}"}],
                        "isError": True,
                    },
                }

        if request_id is None:
            return None

        return self._error_response(request_id, -32601, f"Method not found: {method}")

    def _read_message(self) -> JsonDict | None:
        headers: dict[str, str] = {}
        while True:
            line = sys.stdin.buffer.readline()
            if not line:
                return None
            if line in (b"\r\n", b"\n"):
                break
            key, _, value = line.decode("utf-8").partition(":")
            headers[key.strip().lower()] = value.strip()

        if "content-length" not in headers:
            raise ValueError("Missing Content-Length header")

        length = int(headers["content-length"])
        if length < 0:
            raise ValueError("Invalid Content-Length header")

        body = sys.stdin.buffer.read(length)
        if len(body) != length:
            raise ValueError("Incomplete message body")
        return json.loads(body.decode("utf-8"))

    def _write_message(self, payload: JsonDict) -> None:
        encoded = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        sys.stdout.buffer.write(f"Content-Length: {len(encoded)}\r\n\r\n".encode("ascii"))
        sys.stdout.buffer.write(encoded)
        sys.stdout.buffer.flush()

    def _log_info(self, message: str) -> None:
        LOGGER.info(message)

    def _error_response(self, request_id: Any, code: int, message: str) -> JsonDict:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": code, "message": message},
        }
