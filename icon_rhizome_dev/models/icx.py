from decimal import Decimal

import orjson
from pydantic import BaseModel, root_validator, validator

from icon_rhizome_dev.constants import EXA
from icon_rhizome_dev.models import Result
from icon_rhizome_dev.utils import Utils


class IcxAddress(BaseModel):
    address: str
    audit_tx_hash: str
    balance: Decimal
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


class IcxValidator(BaseModel):
    address: str
    bonded: float
    city: str
    country: str
    delegated: float
    details: str
    email: str
    grade: int
    irep: int
    irep_update_block_height: int
    last_height: int
    name: str
    node_address: str
    p2p_endpoint: str
    penalty: int
    power: float
    status: int
    total_blocks: int
    validated_blocks: int
    website: str

    @root_validator(pre=True)
    def root_validator(cls, values):
        for k, v in values.items():
            try:
                if isinstance(v, str) and v.startswith("0x"):
                    values[k] = Utils.hex_to_int(v)
            except ValueError:
                continue
        print(values)
        return values

    @validator("bonded", "delegated", "power", "irep")
    def loop_to_icx(cls, value) -> float:
        return value / 10**EXA
