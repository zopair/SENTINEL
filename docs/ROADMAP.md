# Roadmap

## v0.1 — Safe core
- [x] Project overview, synthetic graph, bounded exploration, and tests.
- [x] GitHub Actions test workflow.

## v0.2 — Experiment science
- [x] FIFO baseline and deterministic adaptive priority policy.
- [x] Matched-seed comparison and versioned JSONL telemetry.
- [ ] Confidence intervals and documented behavioral datasets.

## v0.3 — Isolated synthetic lab
- [x] Rootless Podman profile, telemetry validation, Bandit, and pip-audit.
- [x] Built-in synthetic agent runtime and Linux containment checks.
- [ ] Sustained hard-quota validation on a dedicated Linux host.
- [ ] Independent escape-oriented review.

## v0.4 — External-agent Containment Gateway
- [x] Immutable image references and rootless-only execution.
- [x] Networkless, read-only, non-root, no-capability profile.
- [x] Bounded CPU, memory, PID, wall-clock, output, and tmpfs.
- [x] Synthetic filesystem/network, PID, tmpfs, output, timeout, and cleanup fixtures.
- [ ] Independent runtime-profile review.
- [ ] External agents remain disabled until independent review passes.

## v0.5 — Adaptive Deception Environment
- [x] Action-conditioned synthetic labyrinth with bounded challenge reformulation.
- [x] Deterministic behavior classification and challenge recommendations.
- [x] Coherent inert synthetic loot, collection events, and apparent-victory telemetry.
- [x] Six repeatable scripted synthetic strategy profiles, including asset collection.
- [ ] Add deception-evasion variations and held-out strategy tests.
- [ ] Compare static and adaptive decoys across larger matched-seed batches.
- [ ] Confidence intervals and uncertainty reporting.

## v0.6 — Optional behavior intelligence
- [ ] Build labeled synthetic behavior datasets.
- [ ] Compare deterministic rules with lightweight classifiers on held-out seeds.
- [ ] Add Keras 3 only as an optional extra if measured benefit justifies its cost.
- [ ] Neural output may recommend challenge difficulty; deterministic controls retain final authority.

## v0.7 — Trusted access research
- [ ] Nonce/signature protocol and replay/relay analysis.
- [ ] TPM2 proof of concept on supported hardware.
- [ ] GGWave transport compared with QR/BLE/NFC.
- [ ] Firmware and secure-boot feasibility study.

## Release gates
Passing tests, dependency and secret scans, documented threat model, reproducible configuration, independent containment review, and explicit status claims. Any real-asset exposure or lab escape blocks release.
