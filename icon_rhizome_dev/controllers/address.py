import asyncio

from starlite import Controller, Request, Template, get

from icon_rhizome_dev.balanced.balanced_loans import BalancedLoans
from icon_rhizome_dev.constants import API_PREFIX, BLOCK_TIME
from icon_rhizome_dev.icx_async import IcxAsync
from icon_rhizome_dev.models.tracker import TrackerAddress
from icon_rhizome_dev.tracker import Tracker


class AddressController(Controller):
    """
    A controller for routes relating to ICX addresses.
    """

    path = f"/address"

    @get(path="/{address:str}/")
    async def get_address(self, address: str, block_number: int = 0) -> Template:
        (address_details, balance, delegations) = await asyncio.gather(
            Tracker.get_address_details(address),
            IcxAsync.get_balance(address, in_icx=True),
            IcxAsync.get_delegation(address, block_number=block_number),
        )

        return Template(
            name="address/index.html",
            context={
                "title": f"{address[:6]}...{address[-6:]}",
                "data": {
                    "address": address,
                    "address_details": address_details,
                    "balance": balance,
                    "delegations": delegations,
                },
            },
        )

    @get(path="/htmx/dapp-overview/{address:str}/")
    async def get_htmx_address_dapp_overview(self, address: str) -> Template:
        """Returns an HTMX component containing overviews for various ICON dApps."""

        async def _get_balanced_overview(address: str):
            loan_position = await BalancedLoans.get_loan_position(address)
            print(loan_position)
            return {"loan_position": loan_position}

        balanced_overview = await _get_balanced_overview(address)

        return Template(
            name="address/htmx/address_dapp-overview.html",
            context={
                "data": {
                    "balanced": balanced_overview,
                },
            },
        )
