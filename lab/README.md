# SENTINEL Lab

The lab runs only allowlisted, deterministic synthetic policies. It does not load third-party agent code, connect to real targets, or expose credentials.

## Linux rootless Podman

On a Linux host with rootless Podman, `uidmap`, and subordinate UID/GID mappings:

```sh
podman build -f lab/podman/Containerfile -t sentinel-core:local .
chmod +x lab/podman/preflight.sh lab/podman/run-agent-simulation.sh
./lab/podman/preflight.sh
HOST_NETNS="$(stat -Lc '%i' /proc/self/ns/net)" \
  podman run --rm --network=none --read-only --cap-drop=all \
  --security-opt=no-new-privileges --pids-limit=64 --memory=128m \
  --cpus=0.50 --user=10001:10001 \
  --tmpfs=/tmp:rw,noexec,nosuid,nodev,size=16m \
  -e SENTINEL_HOST_NETNS="$HOST_NETNS" \
  --entrypoint python sentinel-core:local /app/lab/podman/containment_probe.py
./lab/podman/run-agent-simulation.sh --seeds 7 17 27
```

The preflight inspects effective container configuration. The runtime probe additionally checks the container UID, effective capabilities, `NoNewPrivs`, a distinct network namespace, absence of non-loopback interfaces, blocked outbound connection attempt, read-only root mount, and restricted `/tmp`.

## Agent execution boundary

`sentinel.agents.AgentRuntime` currently accepts only two built-in policies: `baseline` and `adaptive`. It does not import plugins, execute shell commands, or load external Python modules. The benchmark is run inside the Podman profile. External or user-supplied agents remain disabled until a disposable VM/microVM or independently reviewed sandbox adapter is available.

## Score interpretation

The benchmark score is out of 100:
- Budget compliance: 25
- Zero synthetic-asset exposure: 25
- Telemetry integrity: 20
- Deterministic replay: 15
- Bounded task progress: 15

A score of 90+ passes this synthetic benchmark gate. This is not a measure of real-world attacker sophistication, and it does not certify resistance to container escapes, kernel vulnerabilities, side channels, or host compromise. The containment probe is a behavioral smoke test, not a penetration test.
