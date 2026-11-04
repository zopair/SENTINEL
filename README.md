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

# Optional local synthetic-only container run (rootless Podman)
podman build -f lab/podman/Containerfile -t sentinel-core:local .
chmod +x lab/podman/run-synthetic.sh
./lab/podman/run-synthetic.sh
```

## Current prototype
- Deterministic procedural graph generation with FIFO baseline and adaptive priority policies.
- Repeatable multi-seed experiment runner comparing both policies under identical budgets.
- JSON and versioned JSONL event/summary output.
- Metrics: visited/created nodes, deepest level, interaction rate, and step-budget utilization.
- Unit tests for determinism, output schema, and resource limits.

Elapsed runtime is recorded for diagnostics but excluded from policy averages because host scheduling introduces noise. The adaptive policy is an explicit heuristic for controlled experiments, not a validated model of real attacker behavior.

## Safety
Do not connect this prototype to production networks or expose it as a public honeypot. Future external-agent adapters require a disposable isolated lab, deny-by-default egress, resource quotas, and escape testing. The core does not launch agents or execute commands.

## Documentation
- [Architecture](docs/ARCHITECTURE.md)
- [Threat model](docs/THREAT_MODEL.md)
- [Roadmap](docs/ROADMAP.md)
- [Research references](docs/RESEARCH_SOURCES.md)
- [Security policy](SECURITY.md)
- [Lab containment design](lab/CONTAINMENT_DESIGN.md)

MIT License. See [LICENSE](LICENSE).
