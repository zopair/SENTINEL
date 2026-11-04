"""Synthetic-only agent fixture for containment integration tests."""
from __future__ import annotations

import json
import os
import socket
import sys
import time


def read_status(key: str) -> str:
    with open("/proc/self/status", encoding="ascii") as handle:
        for line in handle:
            if line.startswith(key + ":"):
                return line.split(":", 1)[1].strip()
    return ""


def probe() -> None:
    try:
        descriptor = os.open("/etc/sentinel-fixture-write", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except OSError:
        filesystem_write_blocked = True
    else:
        os.close(descriptor)
        os.unlink("/etc/sentinel-fixture-write")
        filesystem_write_blocked = False

    try:
        with socket.create_connection(("192.0.2.1", 80), timeout=0.5):
            network_blocked = False
    except OSError:
        network_blocked = True

    facts = {
        "non_root": os.getuid() != 0,
        "capabilities_zero": int(read_status("CapEff") or "0", 16) == 0,
        "no_new_privileges": read_status("NoNewPrivs") == "1",
        "filesystem_write_blocked": filesystem_write_blocked,
        "network_blocked": network_blocked,
    }
    print(json.dumps(facts, sort_keys=True))


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "probe"
    if mode == "probe":
        probe()
    elif mode == "output":
        sys.stdout.write("x" * 20_000)
    elif mode == "sleep":
        time.sleep(10)
    elif mode == "tmpfs":
        path = "/tmp/sentinel-quota-probe"
        written = 0
        try:
            with open(path, "wb") as handle:
                while written <= 2 * 1024 * 1024:
                    handle.write(b"x" * 65_536)
                    handle.flush()
                    written += 65_536
        except OSError:
            pass
        finally:
            try:
                os.unlink(path)
            except OSError:
                pass
        print(json.dumps({"bytes_written_before_limit": written}))
    elif mode == "process_limit":
        children = []
        for _ in range(96):
            try:
                pid = os.fork()
            except OSError:
                break
            if pid == 0:
                time.sleep(0.4)
                os._exit(0)
            children.append(pid)
        for pid in children:
            try:
                os.waitpid(pid, 0)
            except ChildProcessError:
                pass
        print(json.dumps({"children_created": len(children)}))
    elif mode == "child_sleep":
        pid = os.fork()
        if pid == 0:
            time.sleep(20)
            os._exit(0)
        print(json.dumps({"child_pid": pid}), flush=True)
        time.sleep(20)
    else:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
