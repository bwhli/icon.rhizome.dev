from decimal import Decimal

from pydantic import BaseModel, root_validator


class CpsProposal(BaseModel):
    abstain_voters: int
    abstained_votes: Decimal
    approve_voters: int
    approved_reports: int
    approved_votes: Decimal
    budget_adjustment: int
    contributor_address: str
    ipfs_hash: str
    percentage_completed: int
    project_duration: int
    project_title: str
    reject_voters: int
    rejected_votes: int
    sponsor_address: str
    sponsor_deposit_amount: Decimal
    sponsor_deposit_status: str
    sponsor_vote_reason: str
    sponsored_timestamp: str
    status: str
    submit_progress_report: int
    timestamp: int
    token: str
    total_budget: int
    total_voters: int
    total_votes: Decimal
    tx_hash: str

    @root_validator(pre=True)
    def root_validator(cls, values):
        # Convert hexadecimal to decimal integers.
        for k, v in values.items():
            if v.startswith("0x"):
                try:
                    values[k] = int(v, 16)
                except ValueError:
                    pass
        # Convert loop to ICX.
        values["abstained_votes"] = Decimal(values["abstained_votes"] / 10**18)
        values["approved_votes"] = Decimal(values["approved_votes"] / 10**18)
        values["sponsor_deposit_amount"] = Decimal(values["sponsor_deposit_amount"] / 10**18)  # fmt: skip
        values["total_budget"] = Decimal(values["total_budget"] / 10**18)
        values["total_votes"] = Decimal(values["total_votes"] / 10**18)
        return values
