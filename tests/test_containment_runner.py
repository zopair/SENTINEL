import pytest

from sentinel.containment import AgentRunSpec, ContainmentPolicy, PodmanRunner


IMAGE = "registry.example/sentinel-agent@sha256:" + ("b" * 64)


def _fake_podman(tmp_path, monkeypatch, rootless="true"):
    executable = tmp_path / "podman"
    executable.write_text(
        "#!/usr/bin/env python3\n"
        "import sys, time\n"
        "args = sys.argv[1:]\n"
        "if args and args[0] == 'info':\n"
        + "    print(" + repr(rootless) + ")\n"
        + "elif args and args[0] in ('kill', 'rm'):\n"
        "    raise SystemExit(0)\n"
        "elif args and args[0] == 'run':\n"
        "    mode = args[-1]\n"
        "    if mode == 'emit':\n"
        "        sys.stdout.write('x' * 20000)\n"
        "    elif mode == 'sleep':\n"
        "        time.sleep(3)\n"
        "    else:\n"
        "        print('contained-ok')\n"
    )
    executable.chmod(0o755)
    monkeypatch.setattr(
        "sentinel.containment.podman.shutil.which",
        lambda _name: str(executable),
    )
    return executable


def test_runner_executes_only_after_rootless_check(tmp_path, monkeypatch):
    _fake_podman(tmp_path, monkeypatch)
    result = PodmanRunner().run(AgentRunSpec(image=IMAGE, command=["probe"]))
    assert result.status == "completed"
    assert result.exit_code == 0
    assert result.output.strip() == "contained-ok"


def test_runner_fails_closed_when_rootless_is_not_verified(tmp_path, monkeypatch):
    _fake_podman(tmp_path, monkeypatch, rootless="false")
    with pytest.raises(RuntimeError, match="rootless mode is not verified"):
        PodmanRunner().run(AgentRunSpec(image=IMAGE, command=["probe"]))


def test_runner_enforces_output_ceiling_and_marks_truncation(tmp_path, monkeypatch):
    _fake_podman(tmp_path, monkeypatch)
    policy = ContainmentPolicy(output_limit_bytes=1024)
    result = PodmanRunner().run(AgentRunSpec(image=IMAGE, command=["emit"], policy=policy))
    assert result.status == "output_limit_exceeded"
    assert result.output_truncated is True
    assert len(result.output.encode("utf-8")) == 1024


def test_runner_stops_timed_out_process(tmp_path, monkeypatch):
    _fake_podman(tmp_path, monkeypatch)
    policy = ContainmentPolicy(timeout_seconds=1)
    result = PodmanRunner().run(AgentRunSpec(image=IMAGE, command=["sleep"], policy=policy))
    assert result.status == "timed_out"
    assert result.duration_ms < 5000
