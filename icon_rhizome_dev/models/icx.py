import orjson
from pydantic import BaseModel, validator

from icon_rhizome_dev.constants import EXA
from icon_rhizome_dev.models import Result
from icon_rhizome_dev.utils import Utils


class IcxAddress(BaseModel):
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


class IcxTransaction(BaseModel):
    block_number: int
    block_timestamp: int
    data: str
    from_address: str
    hash: str
    method: str
    status: str
    to_address: str
    transaction_fee: str
    transaction_type: int
    type: str
    value: str

    @validator("data")
    def validate_data(cls, v: str) -> dict:
        try:
            v = orjson.loads(v)
            return v
        except:
            return None

    @validator("transaction_fee")
    def validate_transaction_fee(cls, v: str) -> Result:
        if v == "":
            return Result(default=0, string=Utils.int_to_string(0))
        try:
            v = int(v, 16)
            return Result(default=v, string=Utils.int_to_string(v))
        except ValueError:
            return Result(default=0, string=Utils.int_to_string(0))

    @validator("value")
    def validate_value(cls, v: str) -> Result | None:
        if v == "":
            return Result(default=0, string=Utils.int_to_string(0))
        try:
            v = int(v, 16)
            return Result(default=v, string=Utils.int_to_string(v))
        except ValueError:
            return Result(default=0, string=Utils.int_to_string(0))
