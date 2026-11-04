# SENTINEL
### Adaptive Cyber Deception Research Lab

**The attacker follows the trail. SENTINEL controls where it leads.**

SENTINEL is an open-source cybersecurity research prototype exploring adaptive cyber deception in a bounded, fictional environment. It generates inert synthetic decoy assets, runs controlled exploration policies, and exports reproducible telemetry.

> **Status:** Research prototype · version 0.1.0 · not a production security boundary, public honeypot, authentication system, or certified security control.



## Engineering distinctions

SENTINEL's contribution is not a claim of an entirely new class of deception or a guarantee against advanced attackers. Its value is the combination of controlled synthetic experimentation, explicit resource bounds, reproducible comparisons, and a lightweight hands-on research workflow.

- **From anecdotal demonstrations to falsifiable evaluation:** the comparison pipeline reports paired per-seed differences, descriptive 95% confidence intervals, 10,000-draw paired sign-flip permutation tests, and Holm-adjusted p-values. These methods make assumptions and uncertainty more visible; they do not, by themselves, prove real-world defensive effectiveness.
- **Matched multi-policy benchmarking:** six deterministic exploration policies are evaluated against the same pre-generated synthetic graph for each seed/configuration. This controls an important source of variation and supports paired comparisons; it does not eliminate every possible source of bias, including heuristic/profile co-design.
- **Explicit resource budgets:** hard limits on graph size, depth, steps, branching, input shape, and estimated output volume bound the work the research engine will attempt. These safeguards reduce accidental runaway workloads and malformed-input risk; they are not a universal denial-of-service guarantee.
- **A low-dependency local research lab:** the bilingual browser interface supports illustrative exploration, local JSONL inspection, and optional execution of the real Python engine through a standard-library server bound to `127.0.0.1`. Requests are constrained by host/origin checks, request-size limits, field allowlists, and tighter interactive budgets. No cloud service is required for this workflow.

### Project positioning

SENTINEL is an open-source research framework for studying adaptive cyber deception inside bounded synthetic environments. It combines matched multi-policy experiments, paired statistical reporting, explicit resource ceilings, and a loopback-bound interactive lab to make exploration and decoy-steering behavior easier to inspect, reproduce, and challenge. Its current evidence is synthetic and its adaptive policy is a deterministic heuristic—not a learned adversary or a production-grade security control.

## Research question
Can a deterministic adaptive exploration heuristic change how a scripted explorer spends a fixed interaction budget inside a synthetic decoy graph, compared with non-adaptive and standard search baselines?

This is a narrow, testable question. SENTINEL does not claim that an attacker, including a highly capable AI, can be deceived indefinitely.

## Current capabilities
- Bounded synthetic graph with explicit node, depth, step, and branching budgets.
- Six exploration policies with matched seeds: Static Decoy, Random Walk, Greedy, BFS, DFS, and Adaptive.
- Deterministic scripted behavior profiles (six profiles; not learning agents).
- Fictional decoy documents and synthetic telemetry.
- JSON/JSONL schema 2.0 with paired per-seed differences, Monte Carlo sign-flip tests, and Holm-adjusted p-values.
- Hard configuration ceilings: 4,096 nodes, depth 64, 4,096 steps, and branching factor 1–8.
- Rootless Podman CI containment fixtures; these are tests, not proof of escape-proof isolation.
- Bilingual Browser Research Lab with a loopback-only standard-library server for real Python engine runs and local JSONL analytics.

## Policy comparison
| Policy | Selection rule | Purpose |
|---|---|---|
| Static Decoy | FIFO, no policy reprioritization | Non-adaptive reference control |
| Random Walk | Seeded random frontier selection | Random baseline |
| Greedy | Highest fixed decoy-kind priority | Local heuristic baseline |
| BFS | FIFO frontier | Breadth-first baseline |
| DFS | LIFO frontier | Depth-first baseline |
| Adaptive | Decoy-kind priority combined with depth | SENTINEL heuristic under evaluation |

Every policy receives the same deterministic graph pre-generated from the seed and configuration. Static Decoy uses a fixed identifier ordering without behavior-based reprioritization; BFS uses a FIFO queue. The legacy baseline name remains an alias for BFS.

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

Start the local browser interface in a separate terminal from the source checkout:

~~~bash
sentinel web --port 8765
~~~

Then open `http://127.0.0.1:8765/`. The server is loopback-only.

For reproducibility, preserve the exact command, package version, seed list, and output file with any reported result. The CLI default comparison uses 30 seeds.

## Metrics and statistical reporting
The engine reports nodes created/visited, steps, deepest visited level, interaction rate, budget utilization, elapsed runtime, and the invariant real_asset_exposure=0 for its in-memory model.

The comparison exports per-policy means, standard deviations, descriptive normal-approximation 95% confidence intervals, paired per-seed differences against Static Decoy, two-sided paired sign-flip Monte Carlo p-values (10,000 permutations), and Holm-adjusted p-values across the declared policy/metric family. Runtime is excluded from policy comparisons because it is sensitive to host noise. The intervals are descriptive and the permutation tests depend on exchangeability assumptions; neither establishes real-world effectiveness. Report inconclusive and negative findings.

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
[Browser Research Lab](lab.html) · [Research Guide](docs/RESEARCH_GUIDE.md) · [Validation Protocol](docs/VALIDATION_PROTOCOL.md) · [Architecture](docs/ARCHITECTURE.md) · [Threat Model](docs/THREAT_MODEL.md) · [Roadmap](docs/ROADMAP.md) · [Research references](docs/RESEARCH_SOURCES.md) · [Containment Gateway](docs/CONTAINMENT_GATEWAY.md) · [Security policy](SECURITY.md)

## Browser Visual Lab and JSONL analytics
The browser Research Lab has two clearly separated modes: an illustrative browser model, and an optional real-engine mode served locally by the standard-library HTTP server. Run `sentinel web --port 8765` from a source checkout and open `http://127.0.0.1:8765/`; the server binds to loopback only and accepts bounded allowlisted experiment requests. The JSONL reader parses selected CLI/CI files locally and does not upload them. The static GitHub Pages site cannot execute the Python engine; use the local server for real interactive engine runs. The complete research definitions, metric semantics, statistical assumptions, threat boundaries, and reproduction procedure are in the Research Guide.

## Citation
See CITATION.cff for citation metadata. Cite the exact commit and experiment configuration used.

MIT License. See LICENSE.
