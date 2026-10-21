from __future__ import annotations

from typing import Any

from .contract import GovernanceEvaluatorContract


def handle(
    method: str, params: dict[str, Any], state: dict[str, Any] | None = None
) -> dict[str, Any]:
    state = state or {}
    contract = GovernanceEvaluatorContract(quorum=state.get("quorum", 3))

    for proposal_id, proposal in state.get("proposals", {}).items():
        contract.submit_proposal(
            proposal_id,
            proposal.get("proposal_text", ""),
            proposal.get("metadata", {}),
        )
        for reviewer, score in proposal.get("evaluations", {}).items():
            contract.submit_evaluation(
                proposal_id,
                reviewer,
                score,
                proposal.get("rationales", {}).get(reviewer, ""),
            )
        if proposal.get("finalized"):
            contract.finalize(proposal_id)

    if method == "submit_proposal":
        contract.submit_proposal(
            params["proposal_id"],
            params["proposal_text"],
            params.get("metadata"),
        )
    elif method == "submit_evaluation":
        contract.submit_evaluation(
            params["proposal_id"],
            params["reviewer"],
            params["score"],
            params.get("rationale", ""),
        )
    elif method == "finalize":
        contract.finalize(params["proposal_id"])
    elif method == "get_result":
        return {"ok": True, "result": contract.get_result(params["proposal_id"]), "state": state}
    else:
        return {"ok": False, "error": f"unknown method: {method}", "state": state}

    proposals = {}
    for proposal_id, proposal in contract._proposals.items():
        proposals[proposal_id] = {
            "proposal_text": proposal.proposal_text,
            "metadata": proposal.metadata,
            "evaluations": proposal.evaluations,
            "rationales": proposal.rationales,
            "finalized": proposal.finalized,
            "consensus_score": proposal.consensus_score,
        }

    return {
        "ok": True,
        "state": {
            "quorum": contract.quorum,
            "proposals": proposals,
        },
    }
