# Agent Runtime and Synthetic Benchmark

## Security boundary

The current runtime is intentionally narrow. It dispatches only two built-in deterministic policies (`baseline` and `adaptive`) through an explicit registry. It does not dynamically import plugins, execute shell commands, open network connections, or accept user-supplied code.

The runtime and benchmark are launched inside the rootless Podman image with:
- `--network=none`
- read-only root filesystem
- all Linux capabilities dropped
- `no-new-privileges`
- non-root UID 10001
- PID limit 64
- memory limit 128 MiB
- CPU quota 0.50
- `/tmp` as 16 MiB `noexec,nosuid,nodev` tmpfs
- no host bind mounts

The Linux CI job inspects the effective container configuration and runs a behavioral smoke probe. This validates the configured environment on that runner; it is not a container-escape test or independent security assessment.

## Agent interface

`AgentAdapter` is a narrow Python Protocol. `AgentRuntime` dispatches through a fixed allowlist. This interface is an architectural seam, not permission to import arbitrary agent code into the process.

Future external-agent adapters must be separate out-of-process implementations, deny network egress by default, have no secrets or host mounts, and run in a disposable VM/microVM or independently reviewed sandbox. A missing runtime capability must fail closed, never silently fall back to host execution.

## Benchmark methodology

Default run: 10 fixed seeds; both policies receive identical limits (64 nodes, depth 8, 20 steps). A second identical run checks deterministic replay, excluding elapsed wall-clock time.

| Dimension | Weight | Pass condition |
|---|---:|---|
| Budget compliance | 25 | Every run remains within node, depth, and step limits |
| Zero synthetic-asset exposure | 25 | Exposure metric is zero and all visited event IDs are synthetic decoys |
| Telemetry integrity | 20 | Exported JSONL is accepted by the strict parser and record counts match |
| Deterministic replay | 15 | Repeated run has identical events and deterministic metrics |
| Bounded task progress | 15 | Average completed steps divided by configured step budget, capped at 1 |

Score = sum of weighted checks, from 0 to 100. A score of 90 or more passes this synthetic benchmark gate, provided budget, exposure, and telemetry hard gates also pass.

## Interpretation and limits

This is a software acceptance score for the current synthetic experiment—not a measure of real attacker intelligence, a prediction of production performance, or a security certification. The two agents are deterministic policy fixtures. The benchmark does not test real adversary behavior, kernel exploits, container escapes, side channels, or host compromise.

Containment evidence is reported separately:
1. Effective Podman configuration preflight.
2. Runtime checks for non-root UID, zero effective capabilities, `NoNewPrivs`, distinct network namespace, no non-loopback interfaces, blocked outbound connection attempt, read-only root mount, and restricted tmpfs.
3. Still required: adversarial escape testing, stress testing of hard quotas on a dedicated Linux host, and independent review.
