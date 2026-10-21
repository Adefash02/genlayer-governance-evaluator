from genlayer_governance_evaluator.entrypoint import handle


def test_entrypoint_flow() -> None:
    state = {}

    out = handle(
        "submit_proposal",
        {
            "proposal_id": "p1",
            "proposal_text": "Introduce proposal quality rubric",
            "metadata": {"track": "governance"},
        },
        state,
    )
    assert out["ok"] is True

    state = out["state"]
    state = handle(
        "submit_evaluation",
        {"proposal_id": "p1", "reviewer": "alice", "score": 9.0},
        state,
    )["state"]
    state = handle(
        "submit_evaluation",
        {"proposal_id": "p1", "reviewer": "bob", "score": 7.0},
        state,
    )["state"]
    state = handle(
        "submit_evaluation",
        {"proposal_id": "p1", "reviewer": "carol", "score": 8.0},
        state,
    )["state"]

    out = handle("finalize", {"proposal_id": "p1"}, state)
    assert out["ok"] is True

    result = handle("get_result", {"proposal_id": "p1"}, out["state"])
    assert result["ok"] is True
    assert result["result"]["finalized"] is True
    assert result["result"]["consensus_score"] == 8.0


def test_unknown_method_error() -> None:
    out = handle("nope", {}, {})
    assert out["ok"] is False
    assert "unknown method" in out["error"]
