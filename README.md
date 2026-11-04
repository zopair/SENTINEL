# SENTINEL
### Adaptive Cyber Deception & Trusted Access Architecture

**The attacker follows the trail. SENTINEL controls where it leads.**

SENTINEL is an open-source research prototype for bounded, measurable cyber deception. It generates synthetic decoy environments and records how authorized test agents explore them without connecting experiments to real systems.

> **Status:** Early research prototype. Not a production security boundary, authentication product, public honeypot deployment, or certified security control.

## Principles
- The real system is never part of the maze; only synthetic decoy space evolves.
- No real credentials, customer data, or production endpoints in experiments.
- Explicit node, depth, step, time, process, memory, and output budgets.
- No outbound network or command execution in the deception core.
- Deception supplements—not replaces—access control, isolation, monitoring, and secure boot.

## Quick start
Python 3.10+:
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
sentinel run --seed 7 --steps 20 --max-nodes 64
sentinel labyrinth --seed 7 --actions inspect follow verify enumerate
sentinel profiles --seeds 7 17 27
sentinel compare --seeds 7 17 27 --steps 20 --jsonl
```

## Current prototype
- Deterministic procedural graph with FIFO and adaptive-priority exploration.
- Action-conditioned synthetic labyrinth with deterministic behavior classification and bounded challenge recommendations.
- Five scripted synthetic behavior profiles for repeatable, matched-budget evaluation.
- Rootless Podman CI with configuration checks and bounded fixtures for filesystem/network denial, output, tmpfs, PID pressure, timeout, and cleanup.
- A foundation for future external-agent containment; third-party agents are not integrated or enabled.

Behavior classification and scripted profiles are transparent deterministic experiments, not trained neural models or validated models of real attackers. CI demonstrates only the checks executed; it is not independent escape testing or security certification.

## Safety
Do not connect this prototype to production networks or expose it as a public honeypot. Never pass production credentials or customer data into an agent container. External-agent adapters require independent containment review before implementation.

## Documentation
- [Architecture](docs/ARCHITECTURE.md)
- [Threat model](docs/THREAT_MODEL.md)
- [Roadmap](docs/ROADMAP.md)
- [Research references](docs/RESEARCH_SOURCES.md)
- [Computing and isolation options](docs/COMPUTING_AND_ISOLATION_OPTIONS.md)
- [Open-source tooling inventory](docs/OPEN_SOURCE_TOOLING.md)
- [Agent runtime and benchmark](docs/AGENT_RUNTIME.md)
- [Security policy](SECURITY.md)
- [Lab guide](lab/README.md)
- [Containment Gateway](docs/CONTAINMENT_GATEWAY.md)

MIT License. See [LICENSE](LICENSE).
