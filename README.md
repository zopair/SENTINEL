# SENTINEL
### Adaptive Cyber Deception & Trusted Access Architecture

**The attacker follows the trail. SENTINEL controls where it leads.**

SENTINEL is an open-source research prototype for bounded, measurable cyber deception. It generates synthetic attack surfaces and records how authorized test agents explore them without connecting experiments to real systems.

> **Status:** Early research prototype. Not a production security boundary, authentication product, honeypot deployment, or certified security control.

## Principles
- Synthetic-only content: no real credentials, customer data, or production endpoints.
- Bounded execution: explicit node, depth, step, and time budgets.
- No outbound network or command execution in the core.
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
sentinel compare --seeds 7 17 27 --steps 20 --jsonl
```

## Current prototype
- Deterministic procedural graph generation with FIFO baseline and adaptive priority policies.
- Repeatable multi-seed experiment runner comparing both policies under identical budgets.
- Allowlisted built-in agent runtime with a reproducible 100-point synthetic benchmark.
- Rootless Podman Linux CI job that builds the synthetic image, checks effective settings, probes runtime containment properties, and runs the built-in agents in the container.
- Initial external-agent containment gateway with immutable image digests, rootless-only execution, deny-by-default isolation, bounded resources, and capped output; third-party agents are not yet integrated.
- Linux CI integration exercises a synthetic fixture through the gateway, including filesystem/network denial, output caps, and timeout cleanup.
- JSON and versioned JSONL event/summary output.
- Read-only JSONL telemetry parser with strict record types, schema version checks, field allowlists, and input-size limits.
- Metrics: visited/created nodes, deepest level, interaction rate, and step-budget utilization.

Elapsed runtime is recorded for diagnostics but excluded from policy averages because host scheduling introduces noise. The adaptive policy is an explicit heuristic for controlled experiments, not a validated model of real attacker behavior.

## Computing and isolation
See [Open-Source Computing and Isolation Options](docs/COMPUTING_AND_ISOLATION_OPTIONS.md) and [Agent Runtime and Benchmark](docs/AGENT_RUNTIME.md). The Linux CI sandbox currently runs only built-in deterministic strategies. Third-party agent code remains disabled.

## Safety
Do not connect this prototype to production networks or expose it as a public honeypot. Future external-agent adapters require a disposable isolated lab, deny-by-default egress, resource quotas, and escape testing. The core does not launch agents or execute commands.

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
