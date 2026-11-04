# SENTINEL
### Adaptive Cyber Deception & Trusted Access Architecture

**The attacker follows the trail. SENTINEL controls where it leads.**

SENTINEL is an open-source research prototype for bounded, measurable cyber deception. It generates synthetic attack surfaces and records how authorized test agents explore them without connecting the experiment to real systems.

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
```

## Current prototype
- Deterministic procedural graph generation.
- Synthetic decoy nodes and bounded exploration.
- JSON experiment output and baseline metrics.
- Unit tests for determinism and resource limits.

## Safety
Do not connect this prototype to production networks or expose it as a public honeypot. Future external-agent adapters require a disposable isolated lab, deny-by-default egress, resource quotas, and escape testing. The core does not launch agents or execute commands.

## Documentation
- [Architecture](docs/ARCHITECTURE.md)
- [Threat model](docs/THREAT_MODEL.md)
- [Roadmap](docs/ROADMAP.md)
- [Research references](docs/RESEARCH_SOURCES.md)
- [Security policy](SECURITY.md)

MIT License. See [LICENSE](LICENSE).
