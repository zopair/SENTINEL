"""Rootless Podman runner with fixed isolation controls and bounded output."""
from __future__ import annotations

import os
import secrets
import selectors
import shutil
import subprocess  # nosec B404 - fixed argv only; shell execution is never enabled.
import time

from sentinel.containment.policy import AgentRunSpec, RunResult


class PodmanRunner:
    """Run one pinned image in a disposable, networkless rootless container."""

    def __init__(self, executable: str = "podman") -> None:
        self.executable = executable

    def _resolve_executable(self) -> str:
        path = shutil.which(self.executable)
        if path is None:
            raise RuntimeError("Podman executable was not found")
        return path

    def _require_rootless(self, executable: str) -> None:
        try:
            check = subprocess.run(  # nosec B603 - fixed Podman info argv; shell=False.
                [executable, "info", "--format", "{{.Host.Security.Rootless}}"],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                timeout=10,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise RuntimeError("Unable to verify rootless Podman") from exc
        if check.returncode != 0 or check.stdout.strip().lower() != "true":
            raise RuntimeError("Refusing to run: Podman rootless mode is not verified")

    @staticmethod
    def build_argv(executable: str, name: str, spec: AgentRunSpec) -> list[str]:
        policy = spec.policy
        return [
            executable, "run", "--rm", "--name", name, "--pull=never",
            "--network=none", "--read-only", "--cap-drop=all",
            "--security-opt=no-new-privileges",
            f"--pids-limit={policy.pids_limit}",
            f"--memory={policy.memory_mb}m",
            f"--cpus={float(policy.cpus):.2f}",
            "--user=65532:65532",
            f"--tmpfs=/tmp:rw,noexec,nosuid,nodev,size={policy.tmpfs_mb}m",
            spec.image, *spec.command,
        ]

    def _cleanup(self, executable: str, name: str, process: subprocess.Popen[bytes]) -> None:
        # Kill and remove by generated container name; no user-controlled name is accepted.
        for action in ("kill", "rm"):
            args = [executable, action, name]
            if action == "rm":
                args.insert(2, "--force")
            try:
                subprocess.run(  # nosec B603 - fixed Podman lifecycle argv; shell=False.
                    args, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL, timeout=5, check=False,
                )
            except (OSError, subprocess.TimeoutExpired):
                pass
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=2)

    def run(self, spec: AgentRunSpec) -> RunResult:
        executable = self._resolve_executable()
        self._require_rootless(executable)
        name = "sentinel-agent-" + secrets.token_hex(8)
        argv = self.build_argv(executable, name, spec)
        started = time.monotonic()
        try:
            process = subprocess.Popen(  # nosec B603 - fixed Podman argv; agent args stay inside the container, shell=False.
                argv,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                close_fds=True,
                bufsize=0,
            )
        except OSError as exc:
            raise RuntimeError("Unable to start the isolated Podman run") from exc

        output = bytearray()
        status = "completed"
        truncated = False
        selector = selectors.DefaultSelector()
        if process.stdout is None:
            self._cleanup(executable, name, process)
            raise RuntimeError("Podman output pipe was not created")
        selector.register(process.stdout, selectors.EVENT_READ)
        deadline = started + spec.policy.timeout_seconds
        try:
            while selector.get_map():
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    status = "timed_out"
                    break
                events = selector.select(min(remaining, 0.2))
                if not events and process.poll() is not None:
                    continue
                for key, _ in events:
                    chunk = os.read(key.fd, 65_536)
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    available = spec.policy.output_limit_bytes - len(output)
                    if len(chunk) > available:
                        if available > 0:
                            output.extend(chunk[:available])
                        status = "output_limit_exceeded"
                        truncated = True
                        break
                    output.extend(chunk)
                if status != "completed":
                    break
            if status != "completed":
                self._cleanup(executable, name, process)
            else:
                process.wait(timeout=max(0.1, deadline - time.monotonic()))
        except subprocess.TimeoutExpired:
            status = "timed_out"
            self._cleanup(executable, name, process)
        finally:
            # Also clean up on KeyboardInterrupt or an unexpected host-side exception.
            if process.poll() is None:
                self._cleanup(executable, name, process)
            selector.close()
            if process.stdout is not None:
                process.stdout.close()

        return RunResult(
            status=status,
            exit_code=process.returncode,
            output=output.decode("utf-8", errors="replace"),
            duration_ms=max(0, int((time.monotonic() - started) * 1000)),
            output_truncated=truncated,
        )
