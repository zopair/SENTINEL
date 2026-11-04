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
- [x] Linux CI job for Podman configuration preflight and runtime containment smoke checks (execution result tracked in Actions).
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
