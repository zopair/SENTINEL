# Roadmap

## v0.1 — Safe core
- [x] Project overview and safety boundary.
- [x] Deterministic synthetic graph generator.
- [x] Bounded exploration and structured JSON output.
- [x] Tests for determinism and resource limits.
- [x] GitHub Actions test workflow verified.

## v0.2 — Experiment science
- [x] FIFO baseline and adaptive-priority exploration policies.
- [x] Multi-seed comparison runner with matched budgets.
- [x] Versioned JSONL event and summary export.
- [x] Metrics: exploration depth, visited/created ratio, and budget utilization.
- [ ] Add confidence intervals after collecting larger experiment batches.
- [ ] Validate the adaptive heuristic against documented agent-behavior datasets.

## v0.3 — Isolated agent lab
- [x] Draft rootless Podman profile for synthetic workloads.
- [x] Read-only JSONL telemetry adapter with strict record schemas and bounded input.
- [x] Property-based tests for telemetry input boundaries.
- [x] Development CI gates for Bandit and pip-audit.
- [x] Allowlisted built-in agent runtime and synthetic 100-point benchmark.
- [x] Linux CI job for Podman configuration preflight and runtime containment smoke checks (verified in [Actions run 41762079705](https://github.com/zopair/SENTINEL/actions/runs/41762079705)).
- [ ] Gitleaks CI integration with a reviewed, pinned upstream action/binary.
- [ ] Disposable VM/microVM adapter for third-party authorized agents with deny-by-default egress.
- [ ] Adversarial escape testing and independent containment review.
- [ ] Verify hard CPU, memory, process, storage, and wall-clock enforcement under load on a dedicated Linux host.

## v0.4 — Trusted access research
- [ ] Nonce/signature protocol and replay/relay analysis.
- [ ] TPM2-backed key proof of concept on supported hardware.
- [ ] GGWave transport experiment compared with QR/BLE/NFC.
- [ ] Firmware/secure-boot feasibility study.

## Release gates
Passing tests, dependency and secret scans, documented threat model, reproducible configuration, and explicit feature-status claims. Any real-asset exposure or lab escape blocks release.


## v0.4 — Containment Gateway foundation

- [x] Add immutable run specifications pinned to full SHA-256 image digests.
- [x] Add bounded CPU, memory, PID, wall-clock, output, and tmpfs policy.
- [x] Require rootless Podman and fail closed if rootless mode cannot be verified.
- [x] Enforce networkless, read-only, non-root, no-capability, no-new-privileges execution with no host mounts.
- [x] Bound captured output and clean up the disposable container on timeout or output overflow.
- [ ] Add bounded adversarial fixtures and verify lifecycle cleanup in Linux CI.
- [ ] Add an external-agent adapter only after the adversarial containment gate passes.

The gateway foundation does not yet launch third-party agents by default and is not an independently validated security boundary.
