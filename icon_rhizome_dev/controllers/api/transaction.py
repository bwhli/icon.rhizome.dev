from starlite import Controller, get

from icon_rhizome_dev.constants import API_PREFIX
from icon_rhizome_dev.models.transaction import Transaction
from icon_rhizome_dev.tracker import Tracker


class ApiTransactionController(Controller):
    """
    A controller for routes relating to ICX transactions.
    """

    path = f"{API_PREFIX}/transactions/"

    @get(path="/{tx_hash:str}/")
    async def get_transaction(self, tx_hash: str) -> Transaction:
        transaction = await Tracker.get_transaction(tx_hash)
        return transaction

    @get(path="/")
    async def get_transactions(self) -> list[Transaction]:
        transactions = await Tracker.get_transactions()
        return transactions
