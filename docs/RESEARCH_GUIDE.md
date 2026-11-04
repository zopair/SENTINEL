# SENTINEL Research Guide
## A self-contained technical guide for researchers, reviewers, and security engineers

**Project:** SENTINEL — Adaptive Cyber Deception Research Lab  
**Current scope:** deterministic, bounded, synthetic-only research prototype  
**Primary implementation:** Python 3.10+  
**Browser interface:** GitHub Pages, static and local-first  
**Security classification:** research simulator; not a production honeypot or security boundary

---

## 1. Executive definition

SENTINEL is an experimental environment for studying whether a controlled synthetic decoy space can influence how an automated explorer allocates a limited interaction budget.

The central idea is not to make a real system appear vulnerable, nor to expose real credentials or services. SENTINEL constructs a fictional graph of inert decoy nodes, lets a bounded exploration policy traverse that graph, records the resulting behavior, and compares alternative policies under matched conditions.

The research hypothesis is:

> Under the same synthetic topology, initial seed, and interaction budget, a behavior-conditioned adaptive selection heuristic may produce a different exploration trajectory from fixed-order and conventional graph-search policies.

This is a hypothesis about measurable behavior inside a model. It is not evidence that a real attacker has been diverted, that a learning agent will remain deceived, or that a production environment has been protected.

## 2. What problem is being studied?

Conventional decoy demonstrations often show that an explorer can be made to visit a fake service or document. That observation alone is weak: it does not establish how the decoy changes the explorer's subsequent decisions, how long the interaction persists, how much of the available budget is spent there, or whether the behavior is distinguishable from ordinary graph traversal.

SENTINEL narrows the question into controlled experiments:
1. Construct one synthetic graph from a declared configuration and seed.
2. Give each policy the same graph and the same limits.
3. Record node discoveries and budget-related events.
4. Compare per-policy outcomes across matched seeds.
5. Report uncertainty and paired statistical tests without overstating their meaning.

The system therefore studies **exploration allocation and policy behavior**, not real-world compromise prevention.

## 3. System architecture

The prototype is organized into the following logical components.

### 3.1 Configuration and hard limits
The operator declares:
- `seed`: integer controlling reproducible graph generation and seeded random choices.
- `max_nodes`: maximum number of synthetic nodes, hard-capped at 4,096.
- `max_depth`: maximum graph depth, hard-capped at 64.
- `max_steps`: maximum exploration steps, hard-capped at 4,096.
- `branching_factor`: children per expanded node, restricted to 1–8.

The engine validates configuration before allocating the graph. Seeds must be unique signed 64-bit integers; one experiment accepts at most 1,000 seeds and rejects configurations whose estimated JSONL record count would exceed 100,000. These application-level ceilings are not a substitute for operating-system CPU, memory, process, or wall-clock quotas.

### 3.2 Synthetic graph generator
The graph is generated in memory before a policy begins. Node identifiers and decoy kinds are derived deterministically from the seed, node ordinal, parent identifier, and depth. The generator creates fictional node types such as:
- service
- document
- repository
- dashboard
- credential hint

These are labels for inert synthetic records. They are not endpoints, working credentials, network services, or access mechanisms.

### 3.3 Exploration policy layer
Each policy receives the same pre-generated node set and topology for a given seed and configuration. The policies differ only in how they select the next node from the frontier.

| Policy | Selection behavior | Experimental role |
|---|---|---|
| Static Decoy | Chooses the lowest node identifier in the frontier | Fixed-order non-adaptive control |
| Random Walk | Chooses a seeded pseudo-random frontier item | Random baseline |
| Greedy | Chooses the highest fixed decoy-kind priority | Local heuristic baseline |
| BFS | Removes the oldest frontier item | Breadth-first baseline |
| DFS | Removes the newest frontier item | Depth-first baseline |
| Adaptive | Combines decoy-kind priority and depth | Hand-designed heuristic under evaluation |

The legacy CLI name `baseline` maps to BFS for backward compatibility. Static Decoy and BFS are intentionally separate controls.

The Adaptive score is a transparent hand-written rule:
`priority(kind) × 10 + depth`.
It is not trained, does not learn across sessions, and does not infer an attacker's intent.

### 3.4 Event and telemetry layer
The engine emits ordered events such as:
- `decoy_discovered`
- `decoy_generated`
- `depth_budget_reached`
- `node_budget_reached`
- `step_budget_reached`

Each event contains a sequence number, event type, synthetic node identifier, depth, and explanatory detail. Run summaries contain the configuration and aggregate metrics.

JSONL is the interchange format. Each line is an independent JSON record. Schema 1.0 remains supported for legacy data; schema 2.0 carries the six-policy experiment summaries and paired statistical metadata. Imported JSONL is parsed as untrusted data: the reader validates field sets, types, numeric ranges, record sizes, and record counts. It never executes commands or loads plugins.

### 3.5 Experiment orchestrator
For each seed, the orchestrator builds a configuration and runs all six policies against the same deterministic graph. It then computes:
- per-policy descriptive summaries;
- paired per-seed differences against Static Decoy;
- descriptive 95% normal-approximation intervals;
- two-sided paired sign-flip permutation p-values;
- Holm-adjusted p-values across the reported policy/metric family.

Elapsed wall-clock time is deliberately excluded from policy-effect comparisons because host load and runtime noise can dominate it.

### 3.6 Browser Visual Lab
The static website contains two separate capabilities:
1. **Illustrative browser simulation:** a local visual teaching model. It is not the Python engine and must not be reported as a Python-engine benchmark.
2. **JSONL analytics:** reads a user-selected file locally in the browser. The file is not uploaded to a server. It is intended to inspect real CLI/CI output.

The interface must label illustrative data, imported experiment data, and CI-produced artifacts distinctly. A chart without an identified data source is not experimental evidence.

## 4. Experimental design and fairness

### 4.1 Matched topology
A policy comparison is fair only when all policies in a seed block receive the same graph, the same starting point, and the same limits. SENTINEL pre-generates the graph before policy execution to avoid giving one policy a more favorable topology.

### 4.2 Matched budgets
Keep `max_nodes`, `max_depth`, `max_steps`, and `branching_factor` identical across policies. If any configuration changes, treat it as a new experiment condition.

### 4.3 Seeds are not independent attackers
A seed provides a reproducible synthetic topology. Thirty seeds are a useful exploratory starting point, not a universal sample-size guarantee. The required sample size depends on variance, effect size, test assumptions, and the claim being evaluated.

### 4.4 Behavioral profile bias
Scripted profiles and hand-designed policies can share assumptions. Results from co-designed strategies can overstate generalization. Future evaluations must include held-out strategies that were not used while designing the Adaptive rule.

## 5. Metric definitions

| Metric | Definition | What it does not prove |
|---|---|---|
| `nodes_created` | Number of synthetic graph nodes generated before exploration | Real attack-surface size |
| `nodes_visited` | Unique synthetic nodes discovered by a policy | Attacker displacement from real assets |
| `steps` | Number of unique-node exploration actions | Real-world attacker effort |
| `deepest_visited_level` | Maximum depth among visited nodes | Deception success |
| `interaction_rate` | Visited nodes divided by created nodes | Quality or believability of bait |
| `step_budget_utilization` | Used steps divided by configured step budget | Long-term engagement |
| `elapsed_ms` | Local execution time for a run | Policy superiority; excluded from comparisons |
| `real_asset_exposure` | In-memory model invariant, currently zero | Proof that arbitrary wrappers or deployments are isolated |

The key scientific distinction is between **engagement** (continued interaction with the synthetic environment), **displacement** (evidence that behavior moved away from a defined alternative target), and **deception discovery** (an explicit, validated indication that an agent recognized the synthetic environment). Current core metrics quantify only synthetic exploration proxies. Displacement and discovery are not yet operationally measured.

## 6. Statistical methods and interpretation

### 6.1 Descriptive intervals
For each metric and policy, schema 2.0 reports the mean, population standard deviation, and a normal-approximation 95% interval:
`mean ± 1.96 × SD / sqrt(n)`.

This is a descriptive approximation, not a Student-t interval. It may be unreliable with small samples, skewed distributions, or bounded/discrete metrics.

### 6.2 Paired differences
For every non-reference policy, SENTINEL calculates the metric difference from Static Decoy within each matching seed. The interval is calculated over those paired differences. Positive and negative signs must be interpreted according to the metric; more visits are not automatically better.

### 6.3 Paired sign-flip permutation test
The current implementation performs a two-sided Monte Carlo sign-flip test on the mean paired difference, using 10,000 permutations and a deterministic resampling seed. The plus-one correction prevents a reported Monte Carlo p-value of zero.

This test assumes sign exchangeability under the null. The p-value is not the probability that the null hypothesis is true, does not measure effect size, and does not establish operational security benefit.

### 6.4 Multiple comparisons
Holm step-down adjustment is applied across the 30 reported policy/metric comparisons (five policies against the reference across six metrics). Report both raw and adjusted values. This correction does not protect against additional analyses selected after looking at the data.

### 6.5 Reporting rule
Always publish the seed list, exact command, configuration, commit SHA, Python version, raw JSONL, metric definitions, statistical method, and limitations. Report null, negative, and inconclusive findings. Do not select only favorable metrics.

## 7. Adaptive-agent evaluation: what is missing

The current built-in scripted profiles are not learning agents. A future adaptive-adversary evaluation should test synthetic agents that:
- revisit previously observed nodes;
- compare repeated responses;
- deliberately backtrack;
- track duplicate identifiers and content;
- form and update hypotheses about the environment;
- choose whether to continue, inspect, or withdraw.

The test subject must remain a deterministic in-process fixture or a separately reviewed disposable environment. Arbitrary external agents remain disabled. Do not connect the experiment to public targets, production systems, or real credentials.

The operational definition of deception discovery must be preregistered. Withdrawal, ignoring a decoy, or repeated inspection alone is not proof of discovery.

## 8. Resource-exhaustion evaluation

Application-level limits are enforced before graph allocation. Additional tests should measure:
- peak resident memory;
- CPU time;
- wall-clock time;
- maximum event count and JSONL size;
- behavior at each hard ceiling;
- rejection of oversized, negative, non-integer, NaN, and infinite inputs;
- graceful termination when a limit is reached.

Run stress measurements on a dedicated, disposable test host with OS-level resource limits. Do not run uncontrolled load tests on shared production infrastructure.

## 9. Security model and non-negotiable boundaries

### In scope
- Synthetic-only in-memory graph generation.
- Deterministic built-in policies.
- Strictly bounded local experiment configuration.
- Read-only bounded JSONL ingestion.
- Rootless Podman containment fixtures in CI.

### Out of scope
- Production honeypot deployment.
- Publicly exposed decoy services.
- Real credentials, secrets, customer data, or production-derived artifacts.
- Outbound access to public targets or internal networks.
- Unreviewed external agents, plugins, or arbitrary code execution.
- Claims of escape-proof isolation, permanent deception, or certification.

Stop an experiment if any real asset or secret enters the test, if a network path appears, if a resource ceiling is bypassed, or if the containment profile behaves unexpectedly.

## 10. Reproduction

Install and test:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
```

Run one policy:

```bash
sentinel run --seed 7 --steps 20 --policy adaptive
```

Run the six-policy matched-seed comparison:

```bash
sentinel compare --seeds $(seq 1 30) --steps 20 \
  --max-nodes 64 --max-depth 8 --branching-factor 3 --jsonl > results.jsonl
```

Inspect `results.jsonl` in the browser's local JSONL reader. Do not treat the page's illustrative maze or sample dataset as measured engine output.

## 11. Research roadmap and release gates

1. **Bounded core:** hard application-level ceilings and adversarial input tests.
2. **Statistical validation:** paired effect estimates, permutation tests, and multiple-comparison correction.
3. **Adaptive adversary:** held-out backtracking and learning-oriented synthetic strategies.
4. **Resource profiling:** measured CPU, memory, output, and wall-clock behavior under explicit OS quotas.
5. **Interface validation:** clear separation of illustrative browser simulation and imported engine/CI results.
6. **Runtime research:** evaluate gVisor or Firecracker only when an external-agent runtime is independently reviewed and justified by a threat model.
7. **Enterprise integration:** consider SIEM export only after event semantics, operational value, and deployment isolation are independently validated.

Passing unit tests and CI jobs demonstrates that the tested code paths passed those checks. It does not establish scientific validity, production readiness, or a security guarantee.

## 12. Suggested citation

Cite the exact SENTINEL commit, configuration, seed list, and JSONL artifact used. Do not cite a moving branch name as the sole reproducibility reference.
