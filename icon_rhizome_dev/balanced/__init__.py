import ast
import asyncio
import json
from datetime import datetime

from pydantic import BaseModel
from rich import print

from icon_rhizome_dev.icx_async import IcxAsync
from icon_rhizome_dev.tokens import Tokens
from icon_rhizome_dev.tracker import Tracker


class BalancedDividendClaim(BaseModel):
    contract: str
    symbol: str
    amount: float
    tx_hash: str
    block_number: int
    timestamp: datetime


class Balanced(IcxAsync):

    CONTRACT_BALANCED_DEX = "cxa0af3165c08318e988cb30993b3048335b94af6c"
    CONTRACT_BALANCED_LOANS = "cx66d4d90f5f113eba575bf793570135f9b10cece1"
    CONTRACT_BALANCED_ORACLE = "cx133c6015bb29f692b12e71c1792fddf8f7014652"
    CONTRACT_BALANCED_PEG_STABILITY = "cxa09dbb60dcb62fffbd232b6eae132d730a2aafa6"

    def __init__(self) -> None:
        pass

    @classmethod
    async def get_dividend_claim_amount(cls, tx_hash: str):
        assets_claimed_in_tx = []
        # Get logs with Claimed method in specified transaction.
        logs = await Tracker.get_logs(tx_hash=tx_hash, method="Claimed")
        claimed_log = logs[0]
        assets_claimed = ast.literal_eval(claimed_log.data[2])
        for token_contract, amount in assets_claimed.items():
            dividend_claim = BalancedDividendClaim(
                contract=token_contract,
                symbol=Tokens.get_symbol_by_contract(token_contract),
                amount=amount / 10 ** Tokens.get_decimals_by_contract(token_contract),
                tx_hash=tx_hash,
                block_number=claimed_log.block_number,
                timestamp=claimed_log.block_timestamp,
            )
            assets_claimed_in_tx.append(dividend_claim)
        return assets_claimed_in_tx

    @classmethod
    async def calculate_dividend_claim_usd_amount(
        cls, dividend_claim: BalancedDividendClaim
    ):
        icx_usd_price = await cls.get_icx_usd_price(dividend_claim.block_number)
        return

    @classmethod
    async def get_token_usd_quote(
        cls,
        token_contract: str,
        block_number: int = 0,
    ):
        if Tokens.get_symbol_by_contract(token_contract) == "BALN":
            pass
        elif Tokens.get_symbol_by_contract(token_contract) == "bnUSD":
            pass
        elif Tokens.get_symbol_by_contract(token_contract) == "sICX":
            sicx_icx_price, icx_usd_price = await asyncio.gather(
                *[
                    cls._get_price_by_name("sICX/ICX", block_number=block_number),
                    cls.get_icx_usd_price(block_number=block_number),
                ]
            )
            print(sicx_icx_price, icx_usd_price)
            return sicx_icx_price * icx_usd_price
        return

    @classmethod
    async def _get_price_by_name(cls, pool_name: str, block_number: int = 0):
        params = {"_name": pool_name}
        result = await cls.call(
            cls.CONTRACT_BALANCED_DEX,
            "getPriceByName",
            params,
            block_number=block_number,
        )
        return int(result, 16) / 10**18
