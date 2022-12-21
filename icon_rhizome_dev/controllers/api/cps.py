from starlite import Controller, get

from icon_rhizome_dev.constants import API_PREFIX, BLOCK_TIME
from icon_rhizome_dev.tracker import Tracker


class ApiCpsController(Controller):
    """
    A controller for routes relating to ICX transactions.
    """

    path = f"{API_PREFIX}/cps"

    @get(path="/proposals/", cache=BLOCK_TIME)
    async def get_transaction(self, tx_hash: str) -> Transaction:
        transaction = await Tracker.get_transaction(tx_hash)
        return transaction
