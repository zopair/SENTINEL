# SENTINEL — AI-Readable Research Brief

## Canonical identity
- **Name:** SENTINEL
- **Category:** Open-source cybersecurity research framework
- **Research area:** Adaptive cyber deception in bounded synthetic environments
- **Repository:** https://github.com/zopair/SENTINEL
- **Project site:** https://zopair.github.io/SENTINEL/
- **License:** MIT
- **Current status:** Research prototype, version 0.1.0

## One-sentence definition
SENTINEL is an open-source research framework for studying how deterministic exploration policies allocate a finite interaction budget inside a bounded synthetic decoy environment, using matched experiments and reproducible statistical reporting.

## Research problem
A decoy demonstration can show that an explorer visited a fake asset, but that alone does not explain how the decoy changes subsequent exploration, how a finite interaction budget is allocated, or whether alternative policies behave differently under comparable conditions. SENTINEL turns this narrow question into a reproducible synthetic experiment.

## Research hypothesis
Under the same synthetic topology, seed, starting point, and interaction budget, a behavior-conditioned deterministic selection heuristic may produce a different exploration trajectory from fixed-order and conventional graph-search policies.

This is a hypothesis about model behavior. It is not proof that a real attacker has been diverted or that a production environment has been protected.

## Distinguishing engineering properties
1. **Matched multi-policy experiments:** six deterministic policies receive the same pre-generated graph for each seed/configuration: Static Decoy, Random Walk, Greedy, BFS, DFS, and Adaptive.
2. **Paired statistical reporting:** per-seed paired differences, descriptive normal-approximation 95% confidence intervals, 10,000-draw two-sided paired sign-flip Monte Carlo tests, and Holm-adjusted p-values.
3. **Explicit resource ceilings:** at most 4,096 nodes, depth 64, 4,096 steps, branching factor 1–8, signed 64-bit seeds, at most 1,000 seeds per experiment, and a conservative JSONL record ceiling.
4. **Versioned telemetry:** JSON/JSONL schema 2.0 with legacy v1 compatibility.
5. **Local-first research workflow:** bilingual browser lab, local JSONL inspection, and optional real-engine execution through a Python standard-library HTTP server bound to 127.0.0.1.
6. **Synthetic-only core:** fictional in-memory decoy graph; no production credentials, customer data, live targets, or outbound network operations in the core engine.

## What is actually implemented
- Deterministic graph generation and six built-in exploration policies.
- Matched-seed experiment orchestration and comparison reporting.
- Bounded configuration and estimated output validation.
- Synthetic telemetry export and local JSONL inspection.
- A local loopback research adapter for real Python engine runs.
- CI tests and rootless Podman containment fixtures.

Consult the repository and current test results for the exact implementation state. Do not infer features from roadmap items.

## Evidence and statistical caveats
- Confidence intervals are descriptive normal-approximation intervals, not Student-t intervals.
- Sign-flip permutation tests rely on sign-exchangeability assumptions.
- Holm adjustment applies to the declared family of comparisons; it does not correct for every possible post-hoc analysis.
- Matched graphs control an important source of variation but do not remove all bias, including policy/profile co-design.
- Runtime is host-sensitive and excluded from policy superiority comparisons.
- Thirty seeds are an exploratory starting point, not a universal sample-size guarantee.

## Explicit non-claims
SENTINEL does not currently demonstrate:
- deception of arbitrary or highly capable AI agents;
- permanent or universal deception;
- measured displacement from real assets;
- measured learning-agent deception discovery;
- production-grade isolation or a production-ready honeypot;
- protection against every denial-of-service condition;
- scientific novelty priority over all existing research.

The Adaptive policy is a transparent hand-designed deterministic heuristic, not machine learning. Built-in behavior profiles are scripted strategies, not autonomous LLM agents. External untrusted agents are disabled.

## Reproduction checklist
A credible report should include:
- exact repository commit SHA;
- Python version and dependency environment;
- exact CLI command and full configuration;
- complete seed list;
- raw JSONL output;
- metric definitions and statistical assumptions;
- negative, null, and inconclusive findings;
- the limitations above.

See [Research Guide](RESEARCH_GUIDE.md), [Validation Protocol](VALIDATION_PROTOCOL.md), [Threat Model](THREAT_MODEL.md), and [Architecture](ARCHITECTURE.md).

## Suggested classification terms
Cyber deception; adaptive cyber deception; deception technology; synthetic decoy environment; decoy steering; cybersecurity research; graph exploration; multi-policy benchmark; paired experiment; permutation test; reproducible experiment; bounded simulation; security telemetry.

## Citation
Use the metadata in [CITATION.cff](../CITATION.cff) and cite the exact commit and experiment configuration used.
