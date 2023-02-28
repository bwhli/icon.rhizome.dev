import json
from datetime import datetime

from pydantic import BaseModel, root_validator


class TrackerAddress(BaseModel):
    address: str
    audit_tx_hash: str
    balance: float
    code_hash: str
    contract_type: str
    contract_updated_block: int
    created_timestamp: int
    deploy_tx_hash: str
    is_contract: bool
    is_nft: bool
    is_prep: bool
    is_token: bool
    log_count: int
    name: str
    owner: str
    status: str
    symbol: str
    token_standard: str
    token_transfer_count: int
    transaction_count: int
    transaction_internal_count: int
    type: str


class TrackerLog(BaseModel):
    transaction_hash: str
    log_index: int
    address: str
    block_number: int
    method: str
    data: list | None
    indexed: list | None
    block_timestamp: datetime

    @root_validator(pre=True)
    def root_validator(cls, values):
        data = values["data"]
        indexed = values["indexed"]

        try:
            values["data"] = json.loads(data)
        except:
            values["data"] = None

        try:
            values["indexed"] = json.loads(indexed)
        except:
            values["indexed"] = None

        return values
