# Open-Source Computing and Isolation Options

**Purpose:** identify local, self-hostable building blocks for future SENTINEL lab execution. This is an evaluation shortlist, not an endorsement or a claim that any option has been security-audited by this project.

## Candidate layers

| Project | Layer | Potential SENTINEL use | Trade-off / gate |
|---|---|---|---|
| [Podman](https://github.com/containers/podman) | Rootless OCI containers | Current synthetic-core packaging | Shares host kernel; rootless setup and effective config must be verified |
| [gVisor](https://github.com/google/gvisor) | User-space application kernel (`runsc`) | Stronger syscall isolation for compatible Linux workloads | Runtime compatibility and performance testing required |
| [Firecracker](https://github.com/firecracker-microvm/firecracker) | MicroVM VMM | Disposable per-agent VM boundary | Linux/KVM required; additional guest image, jailer, lifecycle and monitoring work |
| [Kata Containers](https://github.com/kata-containers/kata-containers) | VM-backed OCI runtime | VM isolation behind container workflow | More operational components; likely excessive for current prototype |
| [nsjail](https://github.com/google/nsjail) | Process sandbox (namespaces, cgroups, seccomp) | Narrowly scoped local process restrictions | Not a VM; policy design and kernel compatibility matter |
| [Bubblewrap](https://github.com/containers/bubblewrap) | Namespace sandbox | Lightweight process/filesystem view restriction | Not a complete boundary against kernel vulnerabilities |
| [Wasmtime](https://github.com/bytecodealliance/wasmtime) | WebAssembly runtime | Optional deterministic plugin/transform sandbox | Only useful if workloads can be compiled to WASI; not a general Linux-agent sandbox |
| [Landlock](https://github.com/landlock-lsm/linux) | Linux LSM | Restrict filesystem access for future workers | Kernel support/version and ABI detection required |

## Recommended adoption path

1. **Now:** keep the core dependency-free and use Podman only for the synthetic CLI. Validate its effective runtime configuration before calling the profile verified.
2. **Next:** implement a read-only telemetry ingestion boundary. External agent output is data, never executable instructions.
3. **Linux lab evaluation:** compare rootless Podman + gVisor and nsjail on the same harmless workload; record kernel, runtime, limits, startup cost, and denied operations.
4. **Untrusted agent execution:** require a disposable VM/microVM (Firecracker or Kata where supported), no host mounts, deny-by-default egress, no secrets, hard quotas, snapshots, independent monitoring, and escape testing.
5. **Optional specialized path:** evaluate Wasmtime only for WASI-compatible plugins; do not force it into the main architecture.

## Selection rules

- Prefer local execution and permissive open-source licenses; check each upstream license and release status before vendoring or redistributing.
- Do not depend on hosted sandbox APIs, paid compute, Kubernetes clusters, or vendor-specific control planes for the zero-cost baseline.
- Do not equate open source with secure-by-default. Pin versions, inspect upstream security advisories, test the actual configuration, and document residual risk.
- Never connect experiments to production assets or use real credentials.

## Current decision
No new runtime is added to the Python core. Podman remains an optional packaging layer. gVisor, nsjail, Firecracker, and Wasmtime are candidates for isolated evaluation, not active runtime dependencies.
