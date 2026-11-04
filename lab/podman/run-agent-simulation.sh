#!/bin/sh
set -eu

IMAGE="${SENTINEL_IMAGE:-sentinel-core:local}"
HOST_NETNS="$(stat -Lc '%i' /proc/self/ns/net)"

if ! command -v podman >/dev/null 2>&1; then
  echo "Podman is required." >&2
  exit 127
fi

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
  -e SENTINEL_HOST_NETNS="$HOST_NETNS" \
  --entrypoint python \
  "$IMAGE" -m sentinel.agent_lab "$@"
