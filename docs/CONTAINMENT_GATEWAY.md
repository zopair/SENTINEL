# SENTINEL Containment Gateway — v0.4 foundation

## Purpose

The gateway is the only approved path for a future external-agent execution. It is deliberately separate from the deception engine and built-in synthetic policies.

## Implemented foundation

- Immutable run specification with a full SHA-256 registry digest or local content-addressed image ID; mutable tags such as `latest` are rejected.
- Bounded policy values for memory, CPU, process count, wall-clock time, captured output, and temporary storage.
- Rootless Podman is verified before each run. Failure to verify rootless mode fails closed.
- Fixed runtime profile: no network, read-only root filesystem, all Linux capabilities dropped, no-new-privileges, non-root UID/GID, bounded PID/memory/CPU, and a small noexec/nosuid/nodev tmpfs.
- No host bind mounts, environment forwarding, port publishing, stdin forwarding, or privileged mode.
- Argument-vector execution; the host does not invoke a shell.
- Output is captured with a strict byte ceiling. Timeout or output-limit breach triggers container kill/removal and runner-process cleanup.
- A unique generated container name is used for lifecycle cleanup.

## Deliberate limitations

This is a first gateway foundation, not a claim of complete containment or a production-grade sandbox. It does not yet accept arbitrary source trees, build untrusted images, mount host workspaces, grant network access, or integrate third-party agent frameworks. Images must be built separately in a controlled process and supplied by immutable digest. Do not build an untrusted agent image on a developer workstation and assume rootless image building is a sufficient security boundary.

The runner has not yet undergone independent escape testing. The next stage adds bounded adversarial fixtures and lifecycle tests inside disposable CI environments. A successful run only demonstrates the specific checks that were executed.

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
