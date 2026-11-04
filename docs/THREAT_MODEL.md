# Threat Model

**Scope:** bounded, in-memory research prototype. This document describes the current simulator, not a deployed honeypot or certified isolation boundary.

## Assets and security objectives
- Keep real credentials, customer data, production identities, and production systems outside the experiment.
- Preserve experiment integrity: fixed seeds, explicit budgets, versioned policy definitions, and reproducible output.
- Bound local simulator resource use through hard ceilings: 4,096 nodes, depth 64, 4,096 steps, branching factor 1–8, and signed 64-bit seeds.
- Avoid implying that synthetic interaction proves real-world attacker deception.

## Adversaries and assumptions
The current evaluation uses deterministic scripted strategies and algorithmic exploration policies. It does not yet evaluate arbitrary external agents, adaptive learning attackers, or autonomous LLM agents. The design assumes the Python simulator is run by a trusted operator with synthetic inputs only.

## Trust boundaries
| Boundary | Current status | Required rule |
|---|---|---|
| SENTINEL in-memory core | Implemented | Synthetic graph and fictional assets only |
| Local operator environment | Outside simulator control | Do not provide production secrets or customer data |
| External network | Not used by core engine | No outbound target access |
| Agent/container runtime | Not a production boundary | Do not attach untrusted agents |
| Production systems | Out of scope | Must remain unreachable and disconnected |

## Threats, controls, and residual risk
| Threat | Current control | Residual limitation |
|---|---|---|
| Accidental contact with real assets | Core engine has no network client or production integration | Does not prove safety of arbitrary wrappers or future plugins |
| Resource exhaustion | Hard node, depth, step, branching, seed-count, and estimated telemetry-record budgets | No OS-level CPU/memory isolation in the core |
| Secret leakage into decoys | Fictional in-memory content; synthetic-only policy | Operator could supply sensitive data to future extensions |
| Misleading benchmark claims | Matched seeds, published policy definitions, uncertainty summaries | Heuristic and scripted-agent design may bias results |
| Agent escape or host compromise | External untrusted agents are disabled | No independently reviewed disposable runtime exists |
| Deception discovery | Not currently measured as a learning-agent outcome | Current metrics are exploration proxies, not proof of deception |

## Policy definitions
- **Static Decoy:** FIFO exploration without policy-driven reprioritization; reference control.
- **Random Walk:** reproducible pseudo-random selection from the frontier.
- **Greedy:** selects the frontier node with the highest fixed decoy-kind priority.
- **BFS:** FIFO breadth-first exploration.
- **DFS:** LIFO depth-first exploration.
- **Adaptive:** deterministic heuristic combining decoy-kind priority and depth.

The legacy name baseline remains a backwards-compatible alias for BFS. The graph is pre-generated deterministically before policy execution. Every policy receives the identical node set and topology for a given seed/configuration. Static Decoy uses fixed identifier ordering without behavior-based reprioritization; BFS uses FIFO order.

## Evaluation and interpretation
Experiments use identical seeds and resource budgets across policies. Report per-policy distributions and paired per-seed differences against Static Decoy. The current implementation reports descriptive normal-approximation 95% confidence intervals, paired sign-flip Monte Carlo p-values, and Holm-adjusted values across the declared policy/metric comparisons. These are exploratory; the confidence intervals may be unreliable for small samples or non-normal outcomes, and permutation tests rely on exchangeability assumptions. See the Research Guide for full definitions and interpretation.

Use at least 30 seeds for an initial exploratory run, then increase the sample size based on variance and the intended claim. Report negative and inconclusive results. Keep held-out strategies for later validation because current policies and scripted profiles may share design assumptions.

**Deception Discovery Cost is deferred.** It will only be introduced with learning-capable agents and a preregistered operational definition, such as a measurable classification decision supported by explicit provenance probes. Withdrawal, repeated inspection, or ignoring synthetic loot alone must not be treated as proof that deception was discovered.

## Stop conditions
Stop any future integrated experiment immediately on unapproved network contact, host-mount access, real-secret exposure, quota breach, or suspected isolation failure.

## Non-goals
- Making systems impossible to compromise or deceiving every possible agent indefinitely.
- Replacing IAM, MFA, EDR, segmentation, secure boot, or incident response.
- Attacking, exhausting, or probing third-party infrastructure.
- Running autonomous agents against public targets.
- Claiming production-grade isolation, pre-boot authentication, or security certification.
