# SENTINEL
### Adaptive Cyber Deception Research Lab

**The attacker follows the trail. SENTINEL controls where it leads.**

SENTINEL is an open-source cybersecurity research prototype exploring adaptive cyber deception in a bounded, fictional environment. It generates inert synthetic decoy assets, runs controlled exploration policies, and exports reproducible telemetry.

> **Status:** Research prototype · version 0.1.0 · not a production security boundary, public honeypot, authentication system, or certified security control.

## Research question
Can a deterministic adaptive exploration heuristic change how a scripted explorer spends a fixed interaction budget inside a synthetic decoy graph, compared with non-adaptive and standard search baselines?

This is a narrow, testable question. SENTINEL does not claim that an attacker, including a highly capable AI, can be deceived indefinitely.

## Current capabilities
- Bounded synthetic graph with explicit node, depth, step, and branching budgets.
- Six exploration policies with matched seeds: Static Decoy, Random Walk, Greedy, BFS, DFS, and Adaptive.
- Deterministic scripted behavior profiles (six profiles; not learning agents).
- Fictional decoy documents and synthetic telemetry.
- JSON/JSONL experiment output, per-policy summaries, and paired per-seed comparisons.
- Rootless Podman CI containment fixtures; these are tests, not proof of escape-proof isolation.
- Browser Visual Lab and local JSONL reader on GitHub Pages.

## Policy comparison
| Policy | Selection rule | Purpose |
|---|---|---|
| Static Decoy | FIFO, no policy reprioritization | Non-adaptive reference control |
| Random Walk | Seeded random frontier selection | Random baseline |
| Greedy | Highest fixed decoy-kind priority | Local heuristic baseline |
| BFS | FIFO frontier | Breadth-first baseline |
| DFS | LIFO frontier | Depth-first baseline |
| Adaptive | Decoy-kind priority combined with depth | SENTINEL heuristic under evaluation |

The graph is generated lazily and deterministically under matched seeds and budgets. Static Decoy is a non-adaptive selection control, not a separately pre-generated immutable graph. The legacy baseline name remains an alias for BFS.

## Quick start
Python 3.10+:

~~~bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest

sentinel run --seed 7 --steps 20 --policy adaptive
sentinel profiles --seeds 7 17 27
sentinel compare --seeds $(seq 1 30) --steps 20 --jsonl > results.jsonl
~~~

For reproducibility, preserve the exact command, package version, seed list, and output file with any reported result. The CLI default comparison uses 30 seeds.

## Metrics and statistical reporting
The engine reports nodes created/visited, steps, deepest visited level, interaction rate, budget utilization, elapsed runtime, and the invariant real_asset_exposure=0 for its in-memory model.

The comparison exports per-policy means, standard deviations, descriptive normal-approximation 95% confidence intervals, and paired per-seed differences against Static Decoy. Runtime is excluded from policy comparisons because it is sensitive to host noise. These intervals are exploratory; they do not establish statistical significance or real-world effectiveness. Report inconclusive and negative findings.

## Limitations
- Adaptive is a hand-designed deterministic heuristic, not machine learning.
- Six scripted profiles are not independent evidence of generalization; policy/profile co-design may bias results.
- Current metrics measure synthetic exploration behavior, not whether a learning agent has discovered deception.
- Deception Discovery Cost is deferred until learning-capable agents and an operational detection definition exist.
- No external untrusted agent is enabled; no independently reviewed disposable runtime is provided.
- No real credentials, personal/customer data, production-derived secrets, or live endpoints belong in this lab.
- No claim of permanent or universal deception, production isolation, or security certification is made.

## Safety and threat model
Read the Threat Model before interpreting results or extending the runtime. The core engine is in-memory and does not connect to production systems or perform outbound network operations. Do not connect this prototype to production networks or expose it as a public honeypot.

## Documentation
[Architecture](docs/ARCHITECTURE.md) · [Threat Model](docs/THREAT_MODEL.md) · [Roadmap](docs/ROADMAP.md) · [Research references](docs/RESEARCH_SOURCES.md) · [Containment Gateway](docs/CONTAINMENT_GATEWAY.md) · [Security policy](SECURITY.md)

## Browser Visual Lab and JSONL analytics
The SENTINEL Pages presentation contains an illustrative browser maze and a local JSONL reader. The maze is a visual teaching demo, not the Python engine or a live attack environment. The reader parses a selected file in the browser; it does not upload that file. Sample data is illustrative only. To view real results, generate results.jsonl with the command above and load it in the page.

## Citation
See CITATION.cff for citation metadata. Cite the exact commit and experiment configuration used.

MIT License. See LICENSE.
