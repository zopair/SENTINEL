"""Loopback-only, dependency-free web interface for the real SENTINEL engine."""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
from typing import Any

from sentinel.engine import DeceptionEngine, EngineConfig, POLICIES

MAX_REQUEST_BYTES = 4_096
WEB_MAX_NODES = 256
WEB_MAX_DEPTH = 32
WEB_MAX_STEPS = 256
_ALLOWED_FIELDS = {
    "seed", "policy", "max_nodes", "max_depth", "max_steps", "branching_factor"
}


def execute_run_payload(payload: Any) -> dict[str, Any]:
    """Validate a small JSON request and execute one real in-process engine run."""
    if not isinstance(payload, dict):
        raise ValueError("request body must be a JSON object")
    if set(payload) - _ALLOWED_FIELDS:
        raise ValueError("request contains unsupported fields")

    policy = payload.get("policy", "adaptive")
    if not isinstance(policy, str) or policy not in (*POLICIES, "baseline"):
        raise ValueError("unsupported exploration policy")

    config = EngineConfig(
        seed=payload.get("seed", 7),
        max_nodes=payload.get("max_nodes", 32),
        max_depth=payload.get("max_depth", 8),
        max_steps=payload.get("max_steps", 20),
        branching_factor=payload.get("branching_factor", 3),
    )
    config.validate()
    if config.max_nodes > WEB_MAX_NODES:
        raise ValueError(f"local web runs are limited to {WEB_MAX_NODES} nodes")
    if config.max_depth > WEB_MAX_DEPTH:
        raise ValueError(f"local web runs are limited to depth {WEB_MAX_DEPTH}")
    if config.max_steps > WEB_MAX_STEPS:
        raise ValueError(f"local web runs are limited to {WEB_MAX_STEPS} steps")

    return {
        "source": "python_engine",
        "result": DeceptionEngine(config).run(policy=policy),
    }


def serve(port: int = 8765) -> None:
    """Serve the lab on IPv4 loopback only; never bind to a LAN/public interface."""
    if isinstance(port, bool) or not isinstance(port, int) or not 1024 <= port <= 65535:
        raise ValueError("port must be an integer between 1024 and 65535")

    page = Path(__file__).resolve().parent.parent / "lab.html"
    if not page.is_file():
        raise RuntimeError("lab.html was not found; run SENTINEL from a source checkout")

    allowed_hosts = {f"127.0.0.1:{port}"}
    allowed_origins = {f"http://{host}" for host in allowed_hosts}

    class Handler(BaseHTTPRequestHandler):
        server_version = "SENTINEL-LocalLab"
        sys_version = ""

        def _send(self, status: int, body: bytes, content_type: str) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("X-Frame-Options", "DENY")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'self'; script-src 'unsafe-inline'; "
                "style-src 'unsafe-inline'; connect-src 'self'; "
                "object-src 'none'; base-uri 'none'; frame-ancestors 'none'",
            )
            self.end_headers()
            self.wfile.write(body)

        def _is_loopback_request(self) -> bool:
            host = self.headers.get("Host", "")
            remote = self.client_address[0]
            return host in allowed_hosts and remote == "127.0.0.1"

        def do_GET(self) -> None:
            if not self._is_loopback_request():
                self._send(403, b"Forbidden", "text/plain; charset=utf-8")
                return
            if self.path not in {"/", "/lab.html"}:
                self._send(404, b"Not found", "text/plain; charset=utf-8")
                return
            self._send(200, page.read_bytes(), "text/html; charset=utf-8")

        def do_POST(self) -> None:
            if not self._is_loopback_request():
                self._send(403, b"Forbidden", "text/plain; charset=utf-8")
                return
            if self.path != "/api/run":
                self._send(404, b"Not found", "text/plain; charset=utf-8")
                return
            origin = self.headers.get("Origin")
            if origin not in allowed_origins:
                self._send(403, b"Origin rejected", "text/plain; charset=utf-8")
                return
            if self.headers.get_content_type() != "application/json":
                self._send(415, b"Expected application/json", "text/plain; charset=utf-8")
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                self._send(400, b"Invalid content length", "text/plain; charset=utf-8")
                return
            if length < 1 or length > MAX_REQUEST_BYTES:
                self._send(413, b"Request size limit exceeded", "text/plain; charset=utf-8")
                return
            try:
                raw = self.rfile.read(length)
                payload = json.loads(raw.decode("utf-8"))
                result = execute_run_payload(payload)
                body = json.dumps(result, separators=(",", ":"), allow_nan=False).encode("utf-8")
                self._send(200, body, "application/json; charset=utf-8")
            except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
                body = json.dumps({"error": str(exc)}).encode("utf-8")
                self._send(400, body, "application/json; charset=utf-8")

        def log_message(self, format: str, *args: Any) -> None:
            # Keep local experiment output clean; HTTP errors are returned to the UI.
            return

    server = HTTPServer(("127.0.0.1", port), Handler)
    print(f"SENTINEL local research lab: http://127.0.0.1:{port}/")
    print("Loopback only. Stop with Ctrl+C. No remote agents or network targets are enabled.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping SENTINEL local research lab.")
    finally:
        server.server_close()
