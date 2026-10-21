# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


class GovernanceProposalEvaluator(gl.Contract):
    proposal_count: u256

    def __init__(self):
        self.proposal_count = u256(0)

    @gl.public.view
    def get_proposal_count(self) -> int:
        return self.proposal_count
