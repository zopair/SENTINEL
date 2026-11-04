# SENTINEL Lab

The current lab package runs the synthetic SENTINEL CLI only. It does not launch external agents or connect to real targets.

## Rootless Podman

From the repository root on a Linux host with rootless Podman and Python 3:

```sh
chmod +x lab/podman/preflight.sh lab/podman/run-synthetic.sh
./lab/podman/preflight.sh
./lab/podman/run-synthetic.sh
```

The preflight checks Podman's rootless mode and inspects the effective created-container configuration for network isolation, read-only root filesystem, non-root UID, dropped capabilities, no-new-privileges, PID/memory/CPU limits, and absence of bind mounts.

A passing preflight proves only that the inspected configuration matches the requested profile. It does **not** prove resistance to kernel/runtime exploits, container escape, side channels, or host compromise. No untrusted agent should run in this lab until independent containment tests and review are complete.

See [containment design](CONTAINMENT_DESIGN.md) and [computing/isolation options](../docs/COMPUTING_AND_ISOLATION_OPTIONS.md).
