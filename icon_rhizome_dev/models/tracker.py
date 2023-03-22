import json
from datetime import datetime

from pydantic import BaseModel, root_validator, validator

from icon_rhizome_dev.models import Result
from icon_rhizome_dev.utils import Utils


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
    def root_validator(cls, values: dict) -> dict:
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


class TrackerTokenTransfer(BaseModel):
    token_contract_address: str
    from_address: str
    value: str
    transaction_hash: str
    log_index: int
    block_number: int
    value_decimal: float
    block_timestamp: int
    token_contract_name: str
    transaction_fee: int
    token_contract_symbol: str

    @root_validator(pre=True)
    def root_validator(cls, values: dict) -> dict:
        values["value"] = Utils.hex_to_int(values["value"])
        values["transaction_fee"] = Utils.hex_to_int(values["transaction_fee"])
        return values


class TrackerTransaction(BaseModel):
    hash: str
    log_index: int
    type: str
    method: str
    from_address: str
    to_address: str
    block_number: int
    log_count: int
    version: str
    value: str
    value_decimal: float
    step_limit: str
    timestamp: int
    block_timestamp: int
    nid: str
    nonce: str
    transaction_index: int
    block_hash: str
    transaction_fee: str
    signature: str
    data_type: str
    data: str
    cumulative_step_used: str
    step_used: str
    step_price: str
    score_address: str
    logs_bloom: str
    status: str
