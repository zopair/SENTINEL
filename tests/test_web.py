import pytest

from sentinel.web import execute_run_payload


def test_local_web_executes_the_real_python_engine():
    result = execute_run_payload({
        "seed": 17,
        "policy": "adaptive",
        "max_nodes": 16,
        "max_depth": 4,
        "max_steps": 8,
        "branching_factor": 2,
    })
    assert result["source"] == "python_engine"
    assert result["result"]["metrics"]["real_asset_exposure"] == 0
    assert result["result"]["metrics"]["nodes_created"] <= 16
    assert result["result"]["metrics"]["steps"] <= 8


@pytest.mark.parametrize("payload", [None, [], "not-an-object"])
def test_local_web_rejects_non_object_payloads(payload):
    with pytest.raises(ValueError, match="JSON object"):
        execute_run_payload(payload)


def test_local_web_rejects_unknown_request_fields():
    with pytest.raises(ValueError, match="unsupported fields"):
        execute_run_payload({"policy": "adaptive", "command": "anything"})


def test_local_web_rejects_non_allowlisted_policy():
    with pytest.raises(ValueError, match="unsupported exploration policy"):
        execute_run_payload({"policy": "shell"})


def test_local_web_enforces_smaller_interactive_node_budget():
    with pytest.raises(ValueError, match="limited to 256 nodes"):
        execute_run_payload({"max_nodes": 257})


def test_local_web_rejects_invalid_engine_configuration():
    with pytest.raises(ValueError):
        execute_run_payload({"seed": True})
