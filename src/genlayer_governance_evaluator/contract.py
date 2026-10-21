from __future__ import annotations

from dataclasses import dataclass, field
from statistics import mean
from typing import Any


@dataclass
class ProposalState:
    proposal_text: str
    metadata: dict[str, Any] = field(default_factory=dict)
    evaluations: dict[str, float] = field(default_factory=dict)
    rationales: dict[str, str] = field(default_factory=dict)
    finalized: bool = False
    consensus_score: float | None = None


class GovernanceEvaluatorContract:
    """Consensus-based governance proposal quality evaluator."""

    def __init__(self, *, quorum: int = 3, min_score: float = 0.0, max_score: float = 10.0) -> None:
        if quorum < 1:
            raise ValueError("quorum must be at least 1")
        if min_score >= max_score:
            raise ValueError("min_score must be less than max_score")

        self.quorum = quorum
        self.min_score = min_score
        self.max_score = max_score
        self._proposals: dict[str, ProposalState] = {}

    def submit_proposal(
        self, proposal_id: str, proposal_text: str, metadata: dict[str, Any] | None = None
    ) -> None:
        if not proposal_id:
            raise ValueError("proposal_id is required")
        if proposal_id in self._proposals:
            raise ValueError("proposal already exists")
        self._proposals[proposal_id] = ProposalState(
            proposal_text=proposal_text, metadata=metadata or {}
        )

    def submit_evaluation(
        self, proposal_id: str, reviewer: str, score: float, rationale: str = ""
    ) -> None:
        proposal = self._require_proposal(proposal_id)
        if proposal.finalized:
            raise ValueError("proposal is already finalized")
        if not reviewer:
            raise ValueError("reviewer is required")
        if reviewer in proposal.evaluations:
            raise ValueError("reviewer has already evaluated this proposal")
        if not self.min_score <= score <= self.max_score:
            raise ValueError(f"score must be between {self.min_score} and {self.max_score}")

        proposal.evaluations[reviewer] = float(score)
        proposal.rationales[reviewer] = rationale

    def finalize(self, proposal_id: str) -> float:
        proposal = self._require_proposal(proposal_id)
        if proposal.finalized:
            return proposal.consensus_score or 0.0

        if len(proposal.evaluations) < self.quorum:
            raise ValueError("quorum not reached")

        proposal.consensus_score = round(mean(proposal.evaluations.values()), 4)
        proposal.finalized = True
        return proposal.consensus_score

    def get_result(self, proposal_id: str) -> dict[str, Any]:
        proposal = self._require_proposal(proposal_id)
        return {
            "proposal_id": proposal_id,
            "proposal_text": proposal.proposal_text,
            "metadata": proposal.metadata,
            "evaluation_count": len(proposal.evaluations),
            "quorum": self.quorum,
            "finalized": proposal.finalized,
            "consensus_score": proposal.consensus_score,
            "evaluations": dict(proposal.evaluations),
            "rationales": dict(proposal.rationales),
        }

    def _require_proposal(self, proposal_id: str) -> ProposalState:
        proposal = self._proposals.get(proposal_id)
        if proposal is None:
            raise ValueError("proposal not found")
        return proposal
