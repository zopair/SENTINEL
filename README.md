# SENTINEL
### Adaptive Cyber Deception & Trusted Access Architecture

**The attacker follows the trail. SENTINEL controls where it leads.**

SENTINEL is an open-source cybersecurity research prototype exploring adaptive cyber deception, synthetic honeypot environments, and autonomous-agent behavior evaluation. It creates a bounded fictional labyrinth with inert decoy assets, observes scripted agent exploration, and compares baseline and adaptive policies through reproducible experiments.

> **Status:** Early MVP / research prototype. Not a production security boundary, authentication system, public honeypot deployment, or certified security control.

## Overview

Security defenses commonly detect, block, or contain suspicious activity. SENTINEL explores a complementary research question: **can an agent's exploration be redirected toward believable but entirely synthetic decoy assets, while real assets remain outside the experiment?**

The maze adapts fictional challenges based on observed actions. It offers coherent, cross-referenced decoy documents and records telemetry. This is a testable research idea—not a claim that any agent, including a superintelligent system, can be deceived indefinitely.

## Capabilities

- **Adaptive synthetic labyrinth:** procedural graph with bounded nodes, depth, steps, and challenge recommendations.
- **Behavior classification:** deterministic action-conditioned categories for inspect, follow, enumerate, verify, collect, and wait.
- **Synthetic decoy assets:** fictional reports, service topology, vendor reconciliation, access review, and roadmap documents generated in memory.
- **Apparent victory metrics:** synthetic collection and apparent progress metrics; no real access or value.
- **Repeatable agent simulation:** six scripted behavior profiles, including asset-seeking behavior.
- **Baseline vs adaptive evaluation:** matched seeds and resource budgets; JSON/JSONL telemetry.
- **Containment testing:** rootless Podman CI fixtures test filesystem/network denial, output limits, tmpfs/PID pressure, timeout, and cleanup.
- **Auditable experiments:** deterministic seeds, explicit limits, operator-only provenance manifest.

## Architecture

1. Synthetic environment creates a bounded decoy graph.
2. Built-in agent strategies issue simulated actions.
3. Behavior classifier labels actions deterministically.
4. Adaptive labyrinth updates decoy challenge recommendations.
5. Synthetic loot generator supplies inert fictional documents.
6. Telemetry and experiments compare policies.
7. Containment fixtures exercise local resource and isolation controls.

Neural models, if explored, may propose experiment difficulty only; they do not establish trust, issue credentials, or grant permissions. External untrusted agents remain disabled pending independent containment review.

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

## What to measure

Compare baseline and adaptive policies with matched seeds and budgets. Useful metrics include exploration depth, synthetic asset collection, revisit patterns, dwell/action-count proxies, resource consumption, and activity remaining inside the decoy environment. Use uncertainty estimates and held-out strategies; do not equate synthetic scores with real-world security effectiveness.

## Safety & limitations

- No real credentials, personal/customer data, production-derived secrets, or live endpoints in decoys.
- The deception core does not connect to production systems or execute outbound network operations.
- Resource budgets are explicit and bounded.
- Do not connect to production networks or expose as a public honeypot.
- Never pass production credentials or customer data to agent containers.
- CI success is not proof of escape-proof isolation or security certification.
- No guarantee of permanent or universal deception is claimed.

## Documentation

[Architecture](docs/ARCHITECTURE.md) · [Threat model](docs/THREAT_MODEL.md) · [Roadmap](docs/ROADMAP.md) · [Research references](docs/RESEARCH_SOURCES.md) · [Containment Gateway](docs/CONTAINMENT_GATEWAY.md) · [Security policy](SECURITY.md)

## Search keywords

Cyber deception · deception technology · adaptive honeypot · synthetic honeypot · AI agent security · agentic AI security · autonomous agent behavior · cyber defense research · threat research · red team simulation · blue team · cyber range · decoy assets · security experimentation · Python · open source cybersecurity · containment testing · adaptive cyber defense.

MIT License. See [LICENSE](LICENSE).

## Browser Visual Lab & JSONL Analytics

The GitHub Pages presentation now includes a client-side illustrative maze simulator and a local JSONL analytics reader. The simulator is a visual teaching demo (not the Python engine or a live attack environment). The analytics panel parses `run_summary` records directly in the browser, shows summary metrics and a policy chart, and does not upload the selected file.

To load real experiment results, run:

```bash
sentinel compare --seeds 7 17 27 --steps 20 --jsonl > results.jsonl
```

Open the [SENTINEL Pages presentation](https://zopair.github.io/SENTINEL/) and choose the JSONL file in the analytics panel. The included sample dataset is illustrative only and is not a benchmark claim.
