"""Behavioral checks for the rootless Podman execution profile."""
from __future__ import annotations

import os
import socket
import sys


def check(name: str, passed: bool, detail: str = "") -> bool:
    print(f'{"PASS" if passed else "FAIL"}: {name}' + (f" ({detail})" if detail else ""))
    return passed


def main() -> int:
    results = []
    expected_uid = int(os.environ.get("SENTINEL_CONTAINER_UID", "10001"))
    results.append(check("non-root uid", os.geteuid() == expected_uid, f"euid={os.geteuid()}"))

    try:
        with open("/proc/self/status", encoding="ascii") as handle:
            status = dict(
                line.split(":", 1) for line in handle
                if ":" in line and line.split(":", 1)[0] in {"CapEff", "NoNewPrivs"}
            )
        cap_eff = int(status["CapEff"].strip(), 16)
        no_new_privs = status["NoNewPrivs"].strip() == "1"
    except (OSError, KeyError, ValueError):
        cap_eff, no_new_privs = -1, False
    results.append(check("effective capabilities dropped", cap_eff == 0))
    results.append(check("no-new-privileges active", no_new_privs))

    host_netns = os.environ.get("SENTINEL_HOST_NETNS", "")
    container_netns = str(os.stat("/proc/self/ns/net").st_ino)
    results.append(check(
        "separate network namespace",
        bool(host_netns) and container_netns != host_netns,
        f"host={host_netns}, container={container_netns}",
    ))

    interfaces = sorted(os.listdir("/sys/class/net"))
    results.append(check(
        "no non-loopback network interface",
        set(interfaces) <= {"lo"},
        ",".join(interfaces),
    ))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1.0)
    try:
        connected = sock.connect_ex(("1.1.1.1", 443)) == 0
    except OSError:
        connected = False
    finally:
        sock.close()
    results.append(check("outbound network probe blocked", not connected))

    root_mount_ro = False
    tmp_mount_restricted = False
    try:
        with open("/proc/mounts", encoding="utf-8") as mounts:
            for line in mounts:
                parts = line.split()
                if len(parts) >= 4 and parts[1] == "/":
                    root_mount_ro = "ro" in parts[3].split(",")
                if len(parts) >= 4 and parts[1] == "/tmp":
                    options = set(parts[3].split(","))
                    tmp_mount_restricted = {"noexec", "nosuid", "nodev"} <= options
    except OSError:
        pass
    results.append(check("read-only root filesystem", root_mount_ro))
    results.append(check("restricted tmpfs", tmp_mount_restricted))
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
