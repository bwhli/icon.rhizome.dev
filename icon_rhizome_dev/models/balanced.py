from datetime import datetime

from pydantic import BaseModel, root_validator
from rich import print

from icon_rhizome_dev.constants import EXA
from icon_rhizome_dev.utils import Utils


class BalancedPool(BaseModel):
    pool_id: int


class BalancedLoanAssets(BaseModel):
    bnusd: int
    sicx: int

    @root_validator(pre=True)
    def root_validator(cls, values: dict) -> dict:
        values["bnusd"] = Utils.hex_to_int(values["bnUSD"])
        values["sicx"] = Utils.hex_to_int(values["sICX"])
        return values


class BalancedLoanStanding(BaseModel):
    asset: str
    collateral: int
    ratio: float
    standing: str
    total_debt: int

    @root_validator(pre=True)
    def root_validator(cls, values: dict) -> dict:
        print(values)
        values["collateral"] = Utils.hex_to_int(values["collateral"])
        values["ratio"] = Utils.hex_to_int(values["ratio"]) / 10**18
        values["total_debt"] = Utils.hex_to_int(values["total_debt"])
        print(values)
        return values


class BalancedLoanStandings(BaseModel):
    btcb: BalancedLoanStanding
    eth: BalancedLoanStanding
    sicx: BalancedLoanStanding

    @root_validator(pre=True)
    def root_validator(cls, values: dict) -> dict:
        values["btcb"] = BalancedLoanStanding(**values["BTCB"], asset="btcb")
        values["eth"] = BalancedLoanStanding(**values["ETH"], asset="eth")
        values["sicx"] = BalancedLoanStanding(**values["sICX"], asset="sicx")
        return values


class BalancedLoanHolding(BaseModel):
    base_amount: int
    base_symbol: str
    quote_amount: int
    quote_symbol: str

    @root_validator(pre=True)
    def root_validator(cls, values: dict) -> dict:
        if "BTCB" in values.keys():
            values["base_amount"] = Utils.hex_to_int(values["BTCB"])
            values["base_symbol"] = "btcb"
        elif "ETH" in values.keys():
            values["base_amount"] = Utils.hex_to_int(values["ETH"])
            values["base_symbol"] = "eth"
        elif "sICX" in values.keys():
            values["base_amount"] = Utils.hex_to_int(values["sICX"])
            values["base_symbol"] = "sicx"
        values["quote_amount"] = Utils.hex_to_int(values["bnUSD"])
        values["quote_symbol"] = "bnusd"
        return values


class BalancedLoanHoldings(BaseModel):
    btcb: BalancedLoanHolding
    eth: BalancedLoanHolding
    sicx: BalancedLoanHolding

    @root_validator(pre=True)
    def root_validator(cls, values: dict) -> dict:
        values["btcb"] = BalancedLoanHolding(**values["BTCB"])
        values["eth"] = BalancedLoanHolding(**values["ETH"])
        values["sicx"] = BalancedLoanHolding(**values["sICX"])
        return values


class BalancedLoan(BaseModel):
    address: str
    assets: BalancedLoanAssets
    collateral: int | float
    created: datetime
    holdings: BalancedLoanHoldings
    pos_id: int
    ratio: int
    standing: str
    standings: BalancedLoanStandings
    total_debt: int

    @root_validator(pre=True)
    def root_validator(cls, values: dict) -> dict:
        values["collateral"] = Utils.hex_to_int(values["collateral"])
        values["created"] = datetime.utcfromtimestamp(Utils.hex_to_int(values["created"]) / 1_000_000)  # fmt: skip
        values["pos_id"] = Utils.hex_to_int(values["pos_id"])
        values["ratio"] = Utils.hex_to_int(values["ratio"])
        values["total_debt"] = Utils.hex_to_int(values["total_debt"])
        return values
