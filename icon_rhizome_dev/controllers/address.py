import asyncio

from starlite import Controller, Request, Template, get

from icon_rhizome_dev.constants import API_PREFIX, BLOCK_TIME
from icon_rhizome_dev.icx_async import IcxAsync
from icon_rhizome_dev.models.tracker import TrackerAddress
from icon_rhizome_dev.tracker import Tracker


class AddressController(Controller):
    """
    A controller for routes relating to ICX addresses.
    """

    path = f"/address"

    async def get_balanced_overview(self, address: str) -> dict:
        # Get Balanced loan details.

        return

    @get(path="/{address:str}/")
    async def get_address(self, address: str, block_number: int = 0) -> Template:
        address_details, balance, delegations = await asyncio.gather(
            Tracker.get_address_details(address),
            IcxAsync.get_balance(address, in_icx=True),
            IcxAsync.get_delegation(address, block_number=block_number),
        )
        return Template(
            name="address/index.html",
            context={
                "address": address,
                "address_details": address_details,
                "balance": balance,
                "delegations": delegations,
                "title": f"{address[:6]}...{address[-6:]}",
            },
        )
