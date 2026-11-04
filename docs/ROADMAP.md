# Roadmap

## v0.1 — Safe core
- [x] Project overview and safety boundary.
- [x] Deterministic synthetic graph generation.
- [x] Bounded exploration and structured JSON output.
- [x] Tests for determinism and resource limits.
- [x] GitHub Actions test workflow verified.

## v0.2 — Experiment science
- [x] FIFO baseline and adaptive-priority exploration policies.
- [x] Multi-seed comparison runner with matched budgets.
- [x] Versioned JSONL event and summary export.
- [x] Exploration depth, interaction, and budget metrics.
- [ ] Add confidence intervals after collecting larger experiment batches.
- [ ] Validate the adaptive heuristic against documented agent-behavior datasets.

## v0.3 — Isolated synthetic lab
- [x] Rootless Podman profile and bounded synthetic workload.
- [x] Strict read-only JSONL telemetry adapter and property-based tests.
- [x] Bandit and pip-audit CI gates.
- [x] Allowlisted built-in agent runtime and synthetic benchmark.
- [x] Linux CI preflight and runtime containment smoke checks.
- [ ] Verify hard quotas under sustained load on a dedicated Linux host.
- [ ] Independent escape-oriented review.

## v0.4 — External-agent Containment Gateway
- [x] Immutable run specifications and rootless-only execution.
- [x] Networkless, read-only, non-root, no-capability, no-new-privileges profile.
- [x] Bounded CPU, memory, PID, wall-clock, output, and tmpfs policy.
- [x] Synthetic fixtures for filesystem/network denial, output limits, timeout, PID pressure, and temporary-storage limits.
- [x] Best-effort disposable-container cleanup on timeout, output overflow, interruption, or host-side exception.
- [ ] Independent review of the effective runtime profile.
- [ ] External-agent adapter only after the containment gate passes independent review.

## v0.5 — Adaptive Deception Environment
- [x] Action-conditioned synthetic labyrinth with challenge reformulation.
- [x] Deterministic replay and explicit node/depth/step limits.
- [x] Synthetic interaction telemetry and safety invariants.
- [ ] Add adversary-strategy families and deception-evasion evaluation.
- [ ] Compare static decoys against adaptive labyrinth across larger matched-seed batches.
- [ ] Add confidence intervals and report uncertainty.

## v0.6 — Behavior intelligence (optional)
- [ ] Establish a labeled synthetic behavior dataset and transparent baselines.
- [ ] Evaluate lightweight classifiers before neural models.
- [ ] Add Keras 3 as an optional extra only if it beats deterministic baselines on held-out seeds.
- [ ] Neural inference may recommend challenge difficulty; deterministic policy and crypto verification retain final authority.

## v0.7 — Trusted access research
- [ ] Nonce/signature protocol and replay/relay analysis.
- [ ] TPM2-backed proof of concept on supported hardware.
- [ ] GGWave transport experiment compared with QR/BLE/NFC.
- [ ] Firmware/secure-boot feasibility study.

## Release gates
Passing tests, dependency and secret scans, documented threat model, reproducible configuration, independent containment review, and explicit feature-status claims. Any real-asset exposure or lab escape blocks release.
