import asyncio

from starlite import Controller, Template, get

from icon_rhizome_dev.balanced.balanced_loans import BalancedLoans
from icon_rhizome_dev.controllers.api.v1 import API_PREFIX
from icon_rhizome_dev.icx import Icx
from icon_rhizome_dev.tracker import Tracker


class Api_QuoteController(Controller):
    """
    A controller for API routes for fetching market quotes.
    """

    path = f"{API_PREFIX}/quote"

    @get(path="/icxusd/")
    async def get_icx_usd_quote(self, block_number: int = 0) -> dict:
        icx_usd_quote = await Icx.get_icx_usd_price(block_number)
        return {
            "status": "success",
            "data": {
                "quote": icx_usd_quote,
            },
        }
