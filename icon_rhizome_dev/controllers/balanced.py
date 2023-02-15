import asyncio
import csv
import io
from datetime import datetime, timezone

import pandas as pd
from pydantic import BaseModel, ValidationError, validator
from starlite import Body, Controller, RequestEncodingType, Template, get, post

from icon_rhizome_dev.balanced import Balanced
from icon_rhizome_dev.constants import API_PREFIX, BLOCK_TIME, SM_DISCORD_ADDRESSES
from icon_rhizome_dev.icx_async import IcxAsync
from icon_rhizome_dev.models.icx import IcxTransaction
from icon_rhizome_dev.s3 import S3
from icon_rhizome_dev.tokens import Tokens
from icon_rhizome_dev.tracker import Tracker
from icon_rhizome_dev.utils import Utils


class BalancedController(Controller):
    """
    A controller for routes relating to Balanced.
    """

    path = f"/balanced"

    @get(path="/")
    async def get_balanced(self) -> Template:
        return Template(
            name="balanced/index.html",
            context={},
        )

    @get(path="/htmx/stability-fund/")
    async def get_balanced_htmx_stability_fund(self, block_number: int = 0) -> Template:
        class StabilityFundToken(BaseModel):
            contract: str
            symbol: str
            amount: float

        # Get token contracts for stability fund tokens.
        stability_fund_token_contracts = await Balanced.get_stability_fund_tokens()

        # Initialize a dictionary to map token contract addresses to token balances.
        stability_fund_tokens = []

        # Fetch balance for each token.
        async def _fetch_token_balance(token_contract: str):
            token_balance = await IcxAsync.get_token_balance(
                Balanced.CONTRACT_BALANCED_PEG_STABILITY,
                token_contract,
                block_number=block_number,
            )
            token = StabilityFundToken(
                contract=token_contract,
                symbol=Tokens.get_symbol_by_contract(token_contract),
                amount=token_balance
                / 10 ** Tokens.get_decimals_by_contract(token_contract),
            )
            stability_fund_tokens.append(token)
            return

        await asyncio.gather(
            *[
                _fetch_token_balance(token_contract)
                for token_contract in stability_fund_token_contracts
            ]
        )

        return Template(
            name="balanced/htmx/balanced_stability-fund.html",
            context={
                "stability_fund_tokens": stability_fund_tokens,
            },
        )

    @get(path="/htmx/loans/")
    async def get_balanced_htmx_loans() -> None:
        return

    @get(path="/htmx/swaps/")
    async def get_balanced_htmx_swaps() -> None:
        return
