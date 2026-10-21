import pytest

from genlayer_governance_evaluator import GovernanceEvaluatorContract


def test_submit_proposal_and_result() -> None:
    contract = GovernanceEvaluatorContract(quorum=2)
    contract.submit_proposal("p1", "Improve treasury transparency", {"category": "finance"})

    result = contract.get_result("p1")

    assert result["proposal_text"] == "Improve treasury transparency"
    assert result["metadata"]["category"] == "finance"
    assert result["evaluation_count"] == 0
    assert result["finalized"] is False


def test_duplicate_reviewer_is_rejected() -> None:
    contract = GovernanceEvaluatorContract(quorum=2)
    contract.submit_proposal("p1", "Q")

    contract.submit_evaluation("p1", "alice", 7.0, "solid")

    with pytest.raises(ValueError, match="already evaluated"):
        contract.submit_evaluation("p1", "alice", 8.0, "updated")


def test_finalize_requires_quorum() -> None:
    contract = GovernanceEvaluatorContract(quorum=2)
    contract.submit_proposal("p1", "Q")
    contract.submit_evaluation("p1", "alice", 8.0)

    with pytest.raises(ValueError, match="quorum not reached"):
        contract.finalize("p1")


def test_finalize_produces_consensus_average() -> None:
    contract = GovernanceEvaluatorContract(quorum=3)
    contract.submit_proposal("p1", "Q")
    contract.submit_evaluation("p1", "alice", 6.0)
    contract.submit_evaluation("p1", "bob", 8.0)
    contract.submit_evaluation("p1", "carol", 10.0)

    score = contract.finalize("p1")
    result = contract.get_result("p1")

    assert score == 8.0
    assert result["finalized"] is True
    assert result["consensus_score"] == 8.0
