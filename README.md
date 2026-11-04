# SENTINEL
### Adaptive Cyber Deception & Trusted Access Architecture

**The attacker follows the trail. SENTINEL controls where it leads.**

SENTINEL is an open-source research prototype for bounded, measurable cyber deception. It generates synthetic attack surfaces and records how authorized test agents explore them without connecting experiments to real systems.

> **Status:** Early research prototype. Not a production security boundary, authentication product, honeypot deployment, or certified security control.

## Principles
- Synthetic-only content: no real credentials, customer data, or production endpoints.
- The real system is never part of the maze; only synthetic decoy space evolves.
- Bounded execution: explicit node, depth, step, time, process, memory, and output budgets.
- No outbound network or command execution in the deception core.
- Structured telemetry and reproducible experiments.
- Deception supplements—not replaces—access control, isolation, monitoring, and secure boot.

## Quick start
Python 3.10+:
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
sentinel run --seed 7 --steps 20 --max-nodes 64
sentinel labyrinth --seed 7 --actions inspect follow verify enumerate inspect
sentinel compare --seeds 7 17 27 --steps 20 --jsonl
```

## Current prototype
- Deterministic procedural graph generation with FIFO baseline and adaptive priority policies.
- Adaptive synthetic labyrinth sessions that reformulate decoy challenges from observed test-agent actions under fixed budgets.
- Repeatable multi-seed experiment runner comparing policies under identical budgets.
- Allowlisted built-in agent runtime with a reproducible synthetic benchmark.
- Rootless Podman Linux CI job that checks effective settings, probes runtime containment, and exercises bounded adversarial fixtures.
- Initial external-agent containment gateway with immutable image digests, rootless-only execution, deny-by-default isolation, bounded resources, and capped output; third-party agents are not yet integrated.
- JSON and versioned JSONL telemetry output.

The adaptive labyrinth is deterministic experimental logic, not a trained AI model or a validated model of real attackers. Elapsed runtime is diagnostic only. A successful CI run demonstrates only the specific checks executed; it is not an escape test or security certification.

## Computing and isolation
See [Open-Source Computing and Isolation Options](docs/COMPUTING_AND_ISOLATION_OPTIONS.md), [Agent Runtime and Benchmark](docs/AGENT_RUNTIME.md), and [Containment Gateway](docs/CONTAINMENT_GATEWAY.md).

## Safety
Do not connect this prototype to production networks or expose it as a public honeypot. Future external-agent adapters require a disposable isolated lab, deny-by-default egress, resource quotas, and independent escape-oriented review. Never pass production credentials or real customer data into an agent container.

## Documentation
- [Architecture](docs/ARCHITECTURE.md)
- [Threat model](docs/THREAT_MODEL.md)
- [Roadmap](docs/ROADMAP.md)
- [Research references](docs/RESEARCH_SOURCES.md)
- [Computing and isolation options](docs/COMPUTING_AND_ISOLATION_OPTIONS.md)
- [Open-source tooling inventory and security gates](docs/OPEN_SOURCE_TOOLING.md)
- [Agent runtime and benchmark](docs/AGENT_RUNTIME.md)
- [Security policy](SECURITY.md)
- [Lab guide](lab/README.md)
- [Lab containment design](lab/CONTAINMENT_DESIGN.md)
- [Containment Gateway](docs/CONTAINMENT_GATEWAY.md)

MIT License. See [LICENSE](LICENSE).
