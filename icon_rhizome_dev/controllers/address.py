import asyncio

from pydantic import BaseModel
from starlite import Controller, Template, get

from icon_rhizome_dev.balanced.balanced_loans import BalancedLoans
from icon_rhizome_dev.icx import Icx
from icon_rhizome_dev.tokens import Tokens
from icon_rhizome_dev.tracker import Tracker


class AddressController(Controller):
    """
    A controller for routes relating to ICX addresses.
    """

    path = "/address"

    @get(path="/{address:str}/")
    async def get_address(self, address: str, block_number: int = 0) -> Template:
        (address_details, balance, delegations) = await asyncio.gather(
            Tracker.get_address_details(address),
            Icx.get_balance(address, in_icx=True),
            Icx.get_delegation(address, block_number=block_number),
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

    @get(path="/htmx/assets/{address:str}/")
    async def get_htmx_address_assets(self, address: str) -> Template:

        # Model that represents a row in the Assets table.
        class AssetRow(BaseModel):
            name: str
            symbol: str
            amount: float
            price_in_usd: float
            contract_address: str | None = None

        # Fetch ICX balance and ICX/USD price.
        icx_balance = await Icx.get_balance(address, in_icx=True)
        icx_price_in_usd = await Icx.get_icx_usd_price()

        # Get tokens owned by address.
        token_contract_addresses = await Tracker.get_token_addresses(address)

        assets = await asyncio.gather(
            *[
                Tokens.get_token_metadata(token_contract_address)
                for token_contract_address in token_contract_addresses
            ]
        )

        assets = sorted(assets, key=lambda p: p.symbol)

        # Add ICX to assets list.
        assets.insert(
            0,
            AssetRow(
                name="ICON",
                symbol="ICX",
                amount=icx_balance,
                price_in_usd=icx_price_in_usd,
            ),
        )

        # Add IRC-2 tokens to assets list.

        return Template(
            name="address/htmx/address_assets.html",
            context={
                "data": {"assets": assets},
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
