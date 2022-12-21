from starlite import Controller, get

from icon_rhizome_dev.constants import API_PREFIX, BLOCK_TIME
from icon_rhizome_dev.models.transaction import Transaction
from icon_rhizome_dev.tracker import Tracker


class ApiBalancedController(Controller):
    """
    A controller for routes relating to Balanced.
    """

    path = f"{API_PREFIX}/balanced"

    @get(path="/{pool_id:int}/", cache=BLOCK_TIME)
    async def get_pool(self) -> list[Transaction]:
        return

    @get(path="/", cache=BLOCK_TIME)
    async def get_pools(self) -> list[Transaction]:
        return
