# SENTINEL Architecture

## Mission
Study authorized test-agent behavior inside synthetic decoy environments. The real system is never part of the maze; only generated decoy space changes.

## Layers
1. **Trusted Access Interface (planned):** nonce/signature challenge-response, separate from deception.
2. **Containment Gateway (foundation):** pinned images, rootless Podman, deny-by-default controls, bounded resources, disposable lifecycle.
3. **Behavior Telemetry (prototype):** structured synthetic events and bounded parsing.
4. **Adaptive Deception Engine (prototype):** procedural graph and action-conditioned synthetic labyrinth.
5. **Synthetic Victory & Bait Assets (prototype):** coherent fictional documents, topology maps, operational summaries, reconciliation records, and inert access-review artifacts. Files are generated in memory and collected as simulated loot.
6. **Behavior Policy (prototype):** deterministic classification of synthetic action counters selects challenge families and difficulty; not a trained AI model.
7. **Agent Runtime (synthetic prototype):** allowlisted built-in strategies only; no third-party plugins.
8. **Experiment Orchestrator (prototype):** matched seeds, deterministic replay, apparent-reward telemetry, and transparent benchmark reports.

## Synthetic loot contract
- Artifact contents are internally coherent and cross-reference fictional project and incident IDs.
- Reserved `.invalid` domains are used for fictional hosts and email addresses.
- Credential-like records are explicitly inert placeholders; no password, API key, token, private key, or usable login material is generated.
- Operator provenance is kept in a separate manifest with content hashes.
- The simulated agent receives artifact content; the experiment operator can verify synthetic provenance.
- Files remain in memory in the prototype; no host filesystem writes or external service calls occur.

## Core invariants
- **The real system is never the maze.** No production identity, data, endpoint, or secret is copied into decoys.
- **Perceived progress is not access.** Decoy nodes have no production connectors.
- **The maze evolves, not the attack surface.** Adaptation changes only generated decoys and challenge metadata.
- **Finite resources, repeatable evidence.** Node, depth, step, process, memory, CPU, temporary storage, output, and wall-clock budgets are explicit.

## Boundaries
Only deterministic built-in strategies are used in the in-process runtime. No third-party code, shell commands, network clients, or real target connectors are loaded. Apparent-victory scores measure simulated loot collection, not real attacker motivation or security effectiveness.

## Future external-agent isolation
Use disposable virtual machines or containers, no host mounts, deny-by-default egress, CPU/memory/process/disk/wall-clock quotas, snapshot rollback, independent monitoring, and explicit escape tests. External agents remain disabled until independent review.
