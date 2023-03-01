import orjson
from pydantic import BaseModel, root_validator, validator

from icon_rhizome_dev.constants import EXA
from icon_rhizome_dev.models import Result
from icon_rhizome_dev.utils import Utils


class IcxAddress(BaseModel):
    address: str
    audit_tx_hash: str
    balance: int
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


class IcxDelegation(BaseModel):
    amount: float
    validator_address: str
    validator_name: str = None

    @root_validator(pre=True)
    def root_validator(cls, values):
        values["amount"] = Utils.hex_to_int(values["amount"]) / 10**EXA
        return values


class IcxTokenMetadata(BaseModel):
    contract: str
    decimals: int
    name: str
    symbol: str


class IcxMulticallCall(BaseModel):
    target: str
    metho: str
    params: list[int | str]


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


class IcxValidatorIdentity(BaseModel):
    address: str
    name: str


class IcxValidator(BaseModel):
    address: str
    bonded: float
    bond_ratio: float = None
    city: str
    country: str
    cps: bool = False
    delegated: float
    details: str
    email: str
    grade: int
    reward_daily: int | float = None
    reward_daily_usd: int | float = None
    reward_monthly: int | float = None
    reward_monthly_usd: int | float = None
    name: str
    node_address: str
    p2p_endpoint: str
    penalty: int
    power: float
    productivity: float = None
    rank: int = None
    status: int
    total_blocks: int
    validated_blocks: int
    website: str

    @root_validator(pre=True)
    def root_validator(cls, values):
        # Reassign some keys.
        values["node_address"] = values["nodeAddress"]
        values["p2p_endpoint"] = values["p2pEndpoint"]
        values["total_blocks"] = values["totalBlocks"]
        values["validated_blocks"] = values["validatedBlocks"]

        # Convert hex to integers.
        for k, v in values.items():
            try:
                if isinstance(v, str) and v.startswith("0x"):
                    values[k] = Utils.hex_to_int(v)
            except ValueError:
                continue

        # Calculate bond ratio.
        try:
            values["bond_ratio"] = values["bonded"] / values["delegated"]
        except ZeroDivisionError:
            values["bond_ratio"] = 0

        # Calculate productivity.
        try:
            values["productivity"] = values["validated_blocks"] / values["total_blocks"]
        except ZeroDivisionError:
            values["productivity"] = 0

        return values

    @validator("bonded", "delegated", "power")
    def loop_to_icx(cls, value: int) -> float:
        return value / 10**EXA

    @validator("name")
    def validate_name(cls, value: str) -> str:
        if value.startswith("ICONLEO"):
            return "ICONLEO"
        elif value.startswith("ICXburners"):
            return "ICXburners"
        elif value.startswith("Gilga Capital"):
            return "Gilga Capital"
        elif value.startswith("UNBLOCK"):
            return "UNBLOCK"
        else:
            return value
