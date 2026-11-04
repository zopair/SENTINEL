# Validation Protocol: Adaptive Agent and Resource Resilience

This protocol defines the next research tests for SENTINEL. It is deliberately limited to synthetic, in-process fixtures and disposable local test environments. It does not authorize testing against real systems, public targets, production networks, or third-party agents.

## 1. Test objectives

1. Determine whether the Adaptive heuristic behaves differently from the fixed and graph-search baselines when an explorer revisits, backtracks, and compares prior observations.
2. Determine whether hard configuration ceilings reject resource-amplifying inputs before allocation.
3. Measure whether the engine and JSONL pipeline remain within declared resource budgets.
4. Preserve matched-seed fairness and reproducible test evidence.

## 2. Synthetic adversary profiles

| Profile | Behavior | Required observation |
|---|---|---|
| Linear explorer | Visits the next available node in fixed order | Baseline path and step accounting |
| Backtracking explorer | Returns to a prior node and chooses a different branch | Duplicate/revisit handling; no duplicate unique-visit inflation |
| Repetition explorer | Repeats the same action or node request | Bounded event growth; no unbounded state creation |
| Response-comparison explorer | Compares repeated synthetic metadata | Whether repeated observations reveal stable deterministic patterns |
| Hypothesis explorer | Maintains a simple rule hypothesis from observed node kinds/depths | Number of interactions before a correct/incorrect hypothesis |
| Withdrawal explorer | Stops after a declared synthetic confidence threshold | Withdrawal is recorded separately from deception discovery |

These are test fixtures, not claims about all autonomous agents or LLMs. Each strategy must be specified before results are inspected. Keep at least one held-out strategy family for later evaluation.

## 3. Adaptive-agent fuzz matrix

For each seed and policy:
- vary action order while preserving the same graph;
- revisit nodes at depths 0, 1, and maximum depth;
- issue duplicate observations;
- backtrack one and multiple levels;
- enumerate branches repeatedly;
- submit unknown action labels and malformed metadata to the adapter boundary;
- compare the same node across repeated observations;
- test early withdrawal and budget exhaustion.

Assertions:
- no real or external asset references are created;
- no network operation is attempted by the core engine;
- unique visited-node counts never exceed generated-node counts;
- steps never exceed configured maximum steps;
- depth never exceeds configured maximum depth;
- repeated actions do not create unbounded graph state;
- malformed input is rejected without execution or dynamic loading;
- identical seeds/configurations/policies reproduce identical non-runtime events.

## 4. Resource-exhaustion matrix

Test values immediately below, at, and above each configured hard ceiling:
- nodes: 1, 64, 4,096, and 4,097;
- depth: 0, 8, 64, and 65;
- steps: 0, 20, 4,096, and 4,097;
- branching factor: 1, 3, 8, and 9.

The values above the ceiling must fail validation before graph allocation. Valid maximum configurations must be run only on a disposable host with OS-level memory, CPU, process, and wall-clock limits.

Measure:
- peak resident memory;
- CPU time and wall-clock duration;
- node and event counts;
- serialized JSONL bytes;
- parser time and memory for maximum accepted input;
- cleanup after interrupted or failed test runs.

Do not treat a successful maximum-size run as proof of safety on arbitrary hardware. Publish the host specification and imposed OS quotas.

## 5. Statistical protocol

- Use matched seeds and identical configuration across policies.
- Keep policy definitions and primary metrics fixed before running the experiment.
- Use at least 30 seeds for an exploratory comparison; increase sample size when variance or the intended claim requires it.
- Report per-policy means and uncertainty intervals.
- Report paired per-seed differences against Static Decoy.
- Report raw and Holm-adjusted p-values for the declared family of paired tests.
- Include effect direction and magnitude; statistical significance alone is not practical importance.
- Report null, negative, and inconclusive outcomes.
- Do not treat a browser-generated illustrative sample as experiment data.

## 6. Acceptance criteria

A test batch passes only if:
1. every above-limit configuration is rejected before resource allocation;
2. all in-range runs respect node, depth, and step limits;
3. duplicate/backtracking fixtures cannot cause unbounded graph growth;
4. JSONL parser limits reject oversized and malformed input;
5. the same test inputs reproduce the same non-runtime event sequence;
6. the run records its commit, configuration, seed list, and test environment;
7. no real network, production system, credential, or personal data is used.

A passing batch is evidence only for the tested configurations and fixtures. It is not a production security certification.

## 7. Stop conditions

Immediately stop and preserve logs if:
- any request reaches a non-lab network;
- any production-derived secret or personal data appears;
- a process escapes its intended disposable environment;
- a configured resource limit is exceeded;
- the test harness executes imported data as code;
- the observed behavior differs materially from the declared test protocol.

## 8. Deferred work

Do not add live response-time delays, external agent frameworks, SIEM streaming, MicroVM execution, or dynamic network services until the synthetic adversary and resource tests demonstrate a measured need. Any later runtime expansion requires a separate threat model, independent review, and explicit opt-in.
