# SENTINEL Containment Gateway — v0.4 foundation

## Purpose
The gateway is the only approved path proposed for future external-agent execution. It remains separate from the deception engine and built-in synthetic policies.

## Implemented foundation
- Immutable run specification pinned to a full SHA-256 digest or local content-addressed image ID.
- Bounded memory, CPU, process count, wall-clock time, captured output, and temporary storage.
- Rootless Podman verification; failure to verify rootless mode fails closed.
- Fixed runtime profile: no network, read-only root filesystem, all Linux capabilities dropped, no-new-privileges, non-root UID/GID, no host mounts, no ports, and no environment forwarding.
- Argument-vector execution with no host shell invocation.
- Strict output byte ceiling and disposable-container cleanup on timeout/output overflow.
- Cleanup is attempted from the host-side finally path if execution is interrupted or raises unexpectedly.
- Linux CI fixtures exercise denied filesystem writes and network access, output ceiling, tmpfs quota, PID pressure, timeout, and child-process/container cleanup.

## Deliberate limitations
This is a first gateway foundation, not complete containment or a production-grade sandbox. It does not accept arbitrary source trees, build untrusted images, mount host workspaces, grant network access, or integrate third-party agent frameworks. Images must be built separately in a controlled process and supplied by immutable digest.

CI fixtures validate only the tested behavior and runner lifecycle. They do not constitute kernel escape testing, independent review, or hard-quota validation under sustained adversarial load on a dedicated host. External agents remain disabled until independent escape-oriented review and the remaining release gates pass.

## Example
```python
from sentinel.containment import AgentRunSpec, ContainmentPolicy, PodmanRunner

spec = AgentRunSpec(
    image="registry.example/agent@sha256:" + "<64 lowercase hex characters>",
    command=["python", "-I", "/agent/entrypoint.py"],
    policy=ContainmentPolicy(timeout_seconds=20, output_limit_bytes=65536),
)
result = PodmanRunner().run(spec)
print(result.status, result.exit_code, result.output)
```

Use only images and experiments you are authorized to run. Never pass production credentials or real customer data into an agent container.
