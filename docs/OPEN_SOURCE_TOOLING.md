# Open-Source Execution and Security Tool Inventory

This inventory distinguishes development-time assurance tools from runtime isolation components. A GitHub repository being public does not itself establish that a tool is safe, maintained, compatible, or free of operational cost. Check upstream releases, advisories, transitive dependencies, and licenses before pinning or redistributing binaries.

## Adopted for the current development loop

| Tool | Upstream | Purpose | Integration |
|---|---|---|---|
| pytest | https://github.com/pytest-dev/pytest | Unit/integration test runner | Required in CI |
| Hypothesis | https://github.com/HypothesisWorks/hypothesis | Property-based and edge-case testing | Development extra + CI |
| Bandit | https://github.com/PyCQA/bandit | Python AST security checks | CI gate |
| pip-audit | https://github.com/pypa/pip-audit | Known Python dependency vulnerability audit | CI gate |
| Gitleaks | https://github.com/gitleaks/gitleaks | Secret scanning of source and Git history | Recommended repository/PR scan; pin an audited action or binary before automation |
| Semgrep CE | https://github.com/semgrep/semgrep | Pattern-based multi-language static analysis | Optional local review; tune rules before making it blocking |

## Runtime isolation candidates — not enabled yet

| Tool | Upstream | Layer | Adoption gate |
|---|---|---|---|
| Podman | https://github.com/containers/podman | Rootless OCI containers | Verify effective config on the actual Linux host |
| gVisor | https://github.com/google/gvisor | User-space application kernel | Compatibility, performance, kernel/runtime and escape evaluation |
| nsjail | https://github.com/google/nsjail | Namespaces, cgroups and seccomp process sandbox | Review syscall policy; test on supported Linux kernel |
| Bubblewrap | https://github.com/containers/bubblewrap | Namespace and filesystem sandbox construction | Treat as a policy mechanism, not a complete security boundary |
| Firecracker | https://github.com/firecracker-microvm/firecracker | KVM microVM monitor | Requires KVM-capable Linux host, guest lifecycle and jailer review |
| Wasmtime | https://github.com/bytecodealliance/wasmtime | WebAssembly runtime | Only for compatible WASI workloads; not a general native-agent sandbox |
| Landlock | https://github.com/landlock-lsm/linux | Linux filesystem access-control LSM | Detect kernel ABI and test effective restrictions |

## Security workflow policy

1. Keep runtime dependencies empty; security scanners and property-test packages remain development-only.
2. Run deterministic tests, property-based tests, Bandit, and pip-audit on every push and pull request.
3. Add Gitleaks after pinning the exact reviewed action/binary version and documenting false-positive handling. Do not pipe unverified install scripts into a privileged shell.
4. Treat scanner findings as evidence requiring triage. No scanner is a substitute for threat modeling, code review, or runtime containment tests.
5. Never suppress a finding without a documented rationale and scope.
6. Do not run third-party agents, exploit payloads, or untrusted binaries on the developer host.

## Selection and fallback

- Preferred local baseline: rootless Podman with no network, no host mounts, read-only rootfs, dropped capabilities, no-new-privileges, and hard quotas.
- Stronger candidate: gVisor where supported; compare it against nsjail using the same harmless synthetic workload.
- High-risk untrusted execution: disposable VM/microVM (Firecracker or Kata where the host supports it), deny-by-default egress, no secrets, no shared writable mounts, hard quotas, snapshot/rebuild, and independent monitoring.
- If KVM or gVisor is unavailable, do not silently downgrade the security claim. Keep external-agent execution disabled and continue testing the synthetic core.
- All candidates are open-source projects; the SENTINEL baseline must not require paid hosted sandboxes, paid compute, or commercial control planes.
