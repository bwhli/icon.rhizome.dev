from starlite import Controller, get

from icon_rhizome_dev.constants import API_PREFIX, BLOCK_TIME
from icon_rhizome_dev.models.icx import IcxAddress
from icon_rhizome_dev.tracker import Tracker


class ApiAddressController(Controller):
    """
    A controller for routes relating to ICX addresses.
    """

    path = f"{API_PREFIX}/addresses"

    @get(path="/{address:str}/", cache=BLOCK_TIME)
    async def get_address(self, tx_hash: str) -> IcxAddress:
        transaction = await Tracker.get(tx_hash)
        return transaction

    @get(path="/addresses/", cache=BLOCK_TIME)
    async def get_addressees(self) -> list[IcxAddress]:
        addresses = await Tracker.get_addresses()
        return addresses
