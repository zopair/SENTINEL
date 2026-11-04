# SENTINEL Architecture

## Mission
Study how authorized security agents interact with synthetic decoy environments, while evaluating trusted-access signals as a separate security concern.

## Layers
1. **Trusted Access Interface (planned):** challenge-response proof; not implemented.
2. **Policy Engine (planned):** allow, deny, observe, or redirect decisions.
3. **Procedural Deception Graph (prototype):** synthetic nodes within fixed node/depth/step budgets.
4. **Agent Runtime (synthetic prototype):** allowlisted baseline/adaptive adapters only; no dynamic plugins or arbitrary command execution. Invoked inside the rootless Podman profile in Linux CI.
5. **Experiment Orchestrator (prototype):** matched-seed runs, deterministic replay checks, and a transparent 100-point benchmark.
6. **Telemetry (prototype):** structured event records and summary metrics, parsed through a bounded read-only adapter.
7. **Security Assurance (in progress):** Linux Podman configuration preflight and behavioral smoke checks; adversarial escape testing and independent review remain pending.

## Core invariant
**Perceived progress is not access to a real asset.** The current graph is synthetic and in-memory. It has no network client, shell execution, host filesystem discovery, or credential store.

## Current agent boundary
Only two deterministic, built-in strategies are allowlisted. No third-party code, plugins, shell commands, network clients, or real target connectors are loaded. The benchmark score measures synthetic contract compliance and is not a security certification.

## Trusted access research
A future proof of concept may use a fresh nonce, device-held private key, signed response, expiry, and replay protection. Audio modulation (including GGWave) can transport bytes but is not identity proof, encryption, or secure boot. Hardware-backed key storage and firmware/boot-chain integration require separate hardware validation.

## Isolation requirements for future external agent adapters
Disposable virtual machines or containers; no host mounts; deny-by-default egress; CPU, memory, process, disk, and wall-clock quotas; snapshot rollback; independent monitoring; and explicit escape tests.
