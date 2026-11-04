import pytest

from sentinel.containment import AgentRunSpec, ContainmentPolicy, PodmanRunner


IMAGE = "registry.example/sentinel-agent@sha256:" + ("a" * 64)


def test_default_policy_is_bounded_and_deny_by_default():
    policy = ContainmentPolicy()
    assert policy.memory_mb == 128
    assert policy.cpus == 0.5
    assert policy.pids_limit == 64
    assert policy.timeout_seconds == 30
    assert policy.output_limit_bytes == 262_144
    assert policy.tmpfs_mb == 16


@pytest.mark.parametrize(
    "kwargs",
    [
        {"memory_mb": 63},
        {"memory_mb": 1025},
        {"pids_limit": 0},
        {"timeout_seconds": 301},
        {"output_limit_bytes": 4_194_305},
        {"tmpfs_mb": 0},
        {"cpus": 0.09},
        {"cpus": 2.1},
    ],
)
def test_policy_rejects_out_of_range_limits(kwargs):
    with pytest.raises(ValueError):
        ContainmentPolicy(**kwargs)


def test_policy_rejects_boolean_integer_limits():
    with pytest.raises(ValueError):
        ContainmentPolicy(memory_mb=True)


@pytest.mark.parametrize(
    "image",
    [
        "registry.example/agent:latest",
        "registry.example/agent:v1",
        "registry.example/agent@sha256:abcd",
        "registry.example/agent@sha256:" + ("A" * 64),
    ],
)
def test_run_spec_requires_full_immutable_image_digest(image):
    with pytest.raises(ValueError):
        AgentRunSpec(image=image, command=["agent"])


def test_run_spec_accepts_content_addressed_local_image_id():
    spec = AgentRunSpec(image="sha256:" + ("c" * 64), command=["probe"])
    assert spec.image.startswith("sha256:")


def test_run_spec_requires_bounded_argv_vector():
    with pytest.raises(ValueError):
        AgentRunSpec(image=IMAGE, command="agent")
    with pytest.raises(ValueError):
        AgentRunSpec(image=IMAGE, command=["agent", "bad\x00arg"])
    with pytest.raises(ValueError):
        AgentRunSpec(image=IMAGE, command=["x" * 16_385])


def test_podman_command_has_fixed_isolation_and_no_host_mounts():
    spec = AgentRunSpec(image=IMAGE, command=["python", "-I", "/agent/main.py"])
    argv = PodmanRunner.build_argv("/usr/bin/podman", "sentinel-agent-test", spec)
    assert "--network=none" in argv
    assert "--read-only" in argv
    assert "--cap-drop=all" in argv
    assert "--security-opt=no-new-privileges" in argv
    assert "--user=65532:65532" in argv
    assert not any(arg in {"-v", "--volume", "--mount", "--privileged"} for arg in argv)
    assert argv[-3:] == ["python", "-I", "/agent/main.py"]
