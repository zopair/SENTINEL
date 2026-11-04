# SENTINEL Architecture

## Mission
Study how authorized test agents interact with synthetic decoy environments. The real system is never part of the maze: only isolated, generated decoy space changes in response to observed behavior.

## Layers
1. **Trusted Access Interface (planned):** challenge-response proof; separate from deception and not implemented.
2. **Containment Gateway (foundation):** immutable image references, rootless Podman, deny-by-default controls, bounded resources, and disposable lifecycle.
3. **Behavior Telemetry (prototype):** structured synthetic events and bounded read-only parsing.
4. **Adaptive Deception Engine (prototype):** deterministic procedural graph plus an action-conditioned synthetic labyrinth.
5. **Behavior Policy (research):** current challenge selection is transparent deterministic logic; optional learned classification is a later experiment.
6. **Agent Runtime (synthetic prototype):** allowlisted baseline/adaptive strategies only; no dynamic plugins or arbitrary command execution.
7. **Experiment Orchestrator (prototype):** matched-seed runs, deterministic replay checks, and transparent benchmark reporting.
8. **Security Assurance (in progress):** Linux Podman configuration and behavioral checks; independent escape review remains pending.

## Core invariants
- **The real system is never the maze.** No production identity, data, endpoint, or secret is copied into the decoy environment.
- **Perceived progress is not access.** Labyrinth nodes are synthetic and have no production connectors.
- **The maze evolves, not the attack surface.** Adaptation changes only generated decoy nodes and challenge metadata.
- **Finite resources, repeatable evidence.** Node, depth, step, process, memory, CPU, temporary storage, output, and wall-clock budgets are explicit.

## Current agent boundary
Only two deterministic built-in strategies are allowlisted in the in-process runtime. No third-party code, plugins, shell commands, network clients, or real target connectors are loaded. The benchmark score measures synthetic contract compliance and is not a security certification.

## Trusted access research
A future proof of concept may use a fresh nonce, device-held private key, signed response, expiry, and replay protection. Audio modulation (including GGWave) can transport bytes but is not identity proof, encryption, or secure boot. Hardware-backed key storage and firmware/boot-chain integration require separate hardware validation.

## Isolation requirements for future external agent adapters
Disposable virtual machines or containers; no host mounts; deny-by-default egress; CPU, memory, process, disk, and wall-clock quotas; snapshot rollback; independent monitoring; and explicit escape tests. External agents remain disabled until the containment gate receives independent review.
