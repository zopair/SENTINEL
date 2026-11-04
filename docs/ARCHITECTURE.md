# SENTINEL Architecture

## Mission
Study authorized test-agent behavior inside synthetic decoy environments. The real system is never part of the maze; only generated decoy space changes.

## Layers
1. **Trusted Access Interface (planned):** nonce/signature challenge-response, separate from deception.
2. **Containment Gateway (foundation):** pinned images, rootless Podman, deny-by-default controls, bounded resources, disposable lifecycle.
3. **Behavior Telemetry (prototype):** structured synthetic events and bounded parsing.
4. **Adaptive Deception Engine (prototype):** procedural graph and action-conditioned synthetic labyrinth.
5. **Behavior Policy (prototype):** deterministic classification of synthetic action counters selects challenge families and difficulty; not a trained AI model.
6. **Agent Runtime (synthetic prototype):** allowlisted built-in strategies only; no third-party plugins.
7. **Experiment Orchestrator (prototype):** matched seeds, deterministic replay, transparent benchmark reports.
8. **Security Assurance (in progress):** Linux Podman configuration and behavioral checks; independent escape review remains pending.

## Core invariants
- **The real system is never the maze.** No production identity, data, endpoint, or secret is copied into decoys.
- **Perceived progress is not access.** Decoy nodes have no production connectors.
- **The maze evolves, not the attack surface.** Adaptation changes only generated decoys and challenge metadata.
- **Finite resources, repeatable evidence.** Node, depth, step, process, memory, CPU, temporary storage, output, and wall-clock budgets are explicit.

## Boundaries
Only two deterministic built-in strategies are allowlisted in the in-process runtime. No third-party code, shell commands, network clients, or real target connectors are loaded. Benchmark scores measure synthetic contract compliance, not security certification.

## Trusted access research
A future proof of concept may use a fresh nonce, device-held private key, signed response, expiry, and replay protection. Audio modulation (including GGWave) is transport only, not identity proof, encryption, or secure boot. Hardware-backed keys and firmware integration require separate validation.

## Future external-agent isolation
Use disposable virtual machines or containers, no host mounts, deny-by-default egress, CPU/memory/process/disk/wall-clock quotas, snapshot rollback, independent monitoring, and explicit escape tests. External agents remain disabled until independent review.
