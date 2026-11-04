# Roadmap

## v0.1 — Safe core
- [x] Project overview and safety boundary.
- [x] Deterministic synthetic graph generator.
- [x] Bounded exploration and structured JSON output.
- [x] Tests for determinism and resource limits.
- [ ] Verify CI on GitHub.

## v0.2 — Experiment science
- [ ] Versioned JSONL event export.
- [ ] Baseline vs adaptive policy runner.
- [ ] Metrics: exploration depth, dwell time, decoy interaction rate, false engagement, budget use.
- [ ] Repeated-seed reports and confidence intervals.

## v0.3 — Isolated agent lab
- [ ] Disposable VM/container adapter with deny-by-default egress.
- [ ] CPU, memory, process, storage, and time quotas.
- [ ] Read-only agent telemetry adapter.
- [ ] Escape/containment test suite.

## v0.4 — Trusted access research
- [ ] Nonce/signature protocol and replay analysis.
- [ ] TPM2-backed key proof of concept on supported hardware.
- [ ] GGWave transport experiment compared with QR/BLE/NFC.
- [ ] Firmware/secure-boot feasibility study.

## Release gates
Passing tests, dependency and secret scans, documented threat model, reproducible configuration, and explicit feature-status claims. Any real-asset exposure or lab escape blocks release.
