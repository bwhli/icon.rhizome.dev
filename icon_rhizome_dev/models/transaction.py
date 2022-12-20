import json

import orjson
from pydantic import BaseModel, validator

from icon_rhizome_dev.constants import EXA


class Transaction(BaseModel):
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
    def validate_transaction_fee(cls, v: str) -> float:
        try:
            v = int(v, 16)
            v = v / EXA
            return v
        except:
            return 0

    @validator("value")
    def validate_value(cls, v: str) -> float:
        try:
            v = int(v, 16)
            v = v / EXA
            return v
        except:
            return 0
