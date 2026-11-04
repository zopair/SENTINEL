# SENTINEL
### Adaptive Cyber Deception & Trusted Access Architecture

**The attacker follows the trail. SENTINEL controls where it leads.**

SENTINEL is an open-source research prototype for bounded, measurable cyber deception. It generates synthetic decoy environments and records how authorized test agents explore them without connecting experiments to real systems.

> **Status:** Early research prototype. Not a production security boundary, authentication product, public honeypot deployment, or certified security control.

## Principles
- The real system is never part of the maze; only synthetic decoy space evolves.
- No real credentials, customer data, or production endpoints in experiments.
- Decoy "loot" consists of coherent fictional reports, service maps, reconciliation sheets, and access-review notes generated in memory.
- Apparent reward is tracked as an experiment metric, not real access or real value.
- Explicit node, depth, step, time, process, memory, and output budgets.
- No outbound network or command execution in the deception core.

## Quick start
Python 3.10+:
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
sentinel run --seed 7 --steps 20 --max-nodes 64
sentinel labyrinth --seed 7 --actions inspect follow collect verify enumerate
sentinel profiles --seeds 7 17 27
sentinel compare --seeds 7 17 27 --steps 20 --jsonl
```

## Current prototype
- Deterministic procedural graph with FIFO and adaptive-priority exploration.
- Action-conditioned synthetic labyrinth with behavior classification and bounded challenge recommendations.
- Coherent, cross-referenced, inert synthetic loot; the simulated agent can inspect and collect files, while an operator-only manifest records provenance and content hashes.
- Six scripted synthetic behavior profiles, including an asset collector, for repeatable matched-budget evaluation.
- Rootless Podman CI with bounded fixtures for filesystem/network denial, output, tmpfs, PID pressure, timeout, and cleanup.

Synthetic assets contain no real personal data, live endpoints, usable credentials, or production-derived information. Their "victory score" is only a proxy for apparent progress in a controlled experiment; it does not prove that an autonomous agent can be psychologically manipulated or kept engaged.

## Safety
Do not connect this prototype to production networks or expose it as a public honeypot. Never pass production credentials or customer data into an agent container. External-agent adapters require independent containment review before implementation.

## Documentation
- [Architecture](docs/ARCHITECTURE.md)
- [Threat model](docs/THREAT_MODEL.md)
- [Roadmap](docs/ROADMAP.md)
- [Research references](docs/RESEARCH_SOURCES.md)
- [Security policy](SECURITY.md)
- [Containment Gateway](docs/CONTAINMENT_GATEWAY.md)

MIT License. See [LICENSE](LICENSE).
