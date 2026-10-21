# genlayer-governance-evaluator
Reusable GenLayer Intelligent Contract for consensus-based governance proposal quality evaluation.

## What this repository provides

A reusable Python contract module that evaluates governance proposals using consensus from multiple reviewers.

### Core behavior

- Register governance proposals with metadata
- Accept reviewer quality evaluations per proposal
- Enforce one evaluation per reviewer per proposal
- Finalize when quorum is reached
- Compute deterministic consensus score (mean of reviewer scores)

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e . pytest ruff
pytest
```

## Contract API

`GovernanceEvaluatorContract` supports:

- `submit_proposal(proposal_id, proposal_text, metadata=None)`
- `submit_evaluation(proposal_id, reviewer, score, rationale="")`
- `finalize(proposal_id)`
- `get_result(proposal_id)`

## Entrypoint

Use `genlayer_governance_evaluator.entrypoint.handle(method, params, state)` as a simple stateful dispatcher.
