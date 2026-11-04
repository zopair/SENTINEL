#!/bin/sh
# Verify the effective Podman configuration before running the synthetic image.
set -eu

IMAGE="${SENTINEL_IMAGE:-sentinel-core:local}"
NAME="sentinel-preflight-$$"

if ! command -v podman >/dev/null 2>&1; then
  echo "FAIL: Podman is not installed" >&2
  exit 127
fi
if ! command -v python3 >/dev/null 2>&1; then
  echo "FAIL: python3 is required to inspect Podman JSON" >&2
  exit 127
fi

ROOTLESS="$(podman info --format '{{.Host.Security.Rootless}}' 2>/dev/null || true)"
if [ "$ROOTLESS" != "true" ]; then
  echo "FAIL: Podman is not running rootless (reported: $ROOTLESS)" >&2
  exit 1
fi

cleanup() {
  podman rm -f "$NAME" >/dev/null 2>&1 || true
}
trap cleanup EXIT INT TERM

podman image exists "$IMAGE" || {
  echo "Building synthetic-only image: $IMAGE"
  podman build -f lab/podman/Containerfile -t "$IMAGE" .
}

podman create --name "$NAME" \
  --network=none \
  --read-only \
  --cap-drop=all \
  --security-opt=no-new-privileges \
  --pids-limit=64 \
  --memory=128m \
  --cpus=0.50 \
  --user=10001:10001 \
  --tmpfs=/tmp:rw,noexec,nosuid,nodev,size=16m \
  "$IMAGE" run --seed 7 --steps 1 --max-nodes 2 >/dev/null

podman inspect "$NAME" | python3 -c '
import json, sys
data = json.load(sys.stdin)[0]
host = data.get("HostConfig") or {}
config = data.get("Config") or {}
checks = {
    "network_none": host.get("NetworkMode") == "none",
    "read_only_rootfs": host.get("ReadonlyRootfs") is True,
    "non_root_uid": config.get("User") == "10001:10001",
    "capabilities_dropped": "ALL" in (host.get("CapDrop") or []),
    "no_new_privileges": any("no-new-privileges" in str(x) for x in (host.get("SecurityOpt") or [])),
    "pid_limit_64": host.get("PidsLimit") == 64,
    "memory_limit_128m": host.get("Memory") == 134217728,
    "cpu_limit_0_5": host.get("NanoCpus") == 500000000 or (host.get("CpuQuota") == 50000 and host.get("CpuPeriod") == 100000),
    "no_bind_mounts": not (host.get("Binds") or []),
}
for name, passed in checks.items():
    print(("PASS" if passed else "FAIL") + ": " + name)
if not all(checks.values()):
    sys.exit(1)
'

echo "PASS: effective container configuration matches the requested profile."
echo "NOTE: this is a configuration preflight, not an escape test or security certification."
