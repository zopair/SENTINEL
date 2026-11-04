# Isolated Lab Boundary — Design Draft

**Status: configuration draft; not yet independently validated.**

The current SENTINEL engine is an in-memory synthetic simulator. This lab scaffold packages only that CLI; it does not execute third-party agents, expose a honeypot, or connect to real targets.

## Podman rootless profile
1. Run Podman in rootless mode under a dedicated unprivileged account.
2. Use the provided `lab/podman/Containerfile` to build the synthetic-core image.
3. Run `lab/podman/run-synthetic.sh` with the default image tag.
4. The runner requests: no network, read-only root filesystem, no host mounts, all capabilities dropped, no-new-privileges, non-root UID, PID/memory/CPU limits, and a small no-exec temporary filesystem.

## Build and run

Run the configuration preflight before starting the synthetic container:

```bash
chmod +x lab/podman/preflight.sh lab/podman/run-synthetic.sh
./lab/podman/preflight.sh
```

The preflight inspects the effective created-container settings. It does not start the workload and is not an escape test. See [lab guide](README.md).

```bash
podman build -f lab/podman/Containerfile -t sentinel-core:local .
chmod +x lab/podman/run-synthetic.sh
./lab/podman/run-synthetic.sh
```

## Important limitations
- A container is not a complete security boundary against a hostile kernel/runtime exploit.
- The current runner is for the SENTINEL synthetic CLI only. Do not add an agent binary or mount host credentials.
- No claim is made that the container profile has passed escape testing or independent review.
- For future untrusted agents, prefer disposable VMs or microVMs, rootless execution, deny-by-default networking, immutable snapshots, and independent host monitoring. Firecracker/KVM feasibility depends on the host OS and hardware.
- Any future network allowlist must be explicit, documented, and tested. Default egress remains denied.

## Required release gates before agent execution
- Verify rootless Podman configuration and effective UID.
- Inspect the effective container configuration, not only this command.
- Verify network isolation from inside and outside the container.
- Verify read-only root, absence of host mounts, capability drop, no-new-privileges, and resource limits.
- Run controlled escape/containment tests on disposable hardware.
- Obtain independent review before executing any third-party agent.
