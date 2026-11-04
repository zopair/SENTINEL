#!/bin/sh
set -eu

IMAGE="${SENTINEL_IMAGE:-sentinel-core:local}"
SEED="${SENTINEL_SEED:-7}"
STEPS="${SENTINEL_STEPS:-20}"
MAX_NODES="${SENTINEL_MAX_NODES:-64}"

if ! command -v podman >/dev/null 2>&1; then
  echo "Podman is required. Install it and use rootless mode." >&2
  exit 127
fi

# No host mounts, no network, read-only root filesystem, non-root UID,
# dropped Linux capabilities, no-new-privileges, and explicit resource caps.
exec podman run --rm \
  --network=none \
  --read-only \
  --cap-drop=all \
  --security-opt=no-new-privileges \
  --pids-limit=64 \
  --memory=128m \
  --cpus=0.50 \
  --user=10001:10001 \
  --tmpfs=/tmp:rw,noexec,nosuid,nodev,size=16m \
  "$IMAGE" run \
  --seed "$SEED" \
  --steps "$STEPS" \
  --max-nodes "$MAX_NODES"
