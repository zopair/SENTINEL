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
- [x] Draft rootless Podman profile for the synthetic core only (not agent isolation validation).
- [x] Read-only JSONL telemetry adapter with bounded input and strict schema validation.
- [x] Documented open-source computing/isolation shortlist and adoption gates.
- [ ] Disposable VM/container adapter for authorized agents with deny-by-default egress.
- [ ] Effective runtime configuration preflight and containment verification.
- [ ] CPU, memory, process, storage, and wall-clock quotas verified on a Linux lab host.
- [ ] Escape/containment test suite.
- [ ] Independent review of isolation design before external-agent execution.

## v0.4 — Trusted access research
- [ ] Nonce/signature protocol and replay/relay analysis.
- [ ] TPM2-backed key proof of concept on supported hardware.
- [ ] GGWave transport experiment compared with QR/BLE/NFC.
- [ ] Firmware/secure-boot feasibility study.

## Release gates
Passing tests, dependency and secret scans, documented threat model, reproducible configuration, and explicit feature-status claims. Any real-asset exposure or lab escape blocks release.
