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
    else:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
