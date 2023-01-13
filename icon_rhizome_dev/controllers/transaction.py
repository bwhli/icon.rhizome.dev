from starlite import Controller, get

from icon_rhizome_dev.constants import API_PREFIX, BLOCK_TIME
from icon_rhizome_dev.models.icx import IcxTransaction
from icon_rhizome_dev.tracker import Tracker


class TransactionController(Controller):
    """
    A controller for routes relating to ICX transactions.
    """

    path = f"{API_PREFIX}/transactions"

    @get(path="/{tx_hash:str}/", cache=BLOCK_TIME)
    async def get_transaction(self, tx_hash: str) -> IcxTransaction:
        """
        Returns details about an ICX transaction.

        Args:
            tx_hash: An ICX transaction hash.
        """
        transaction = await Tracker.get_transaction(tx_hash)
        return transaction

    @get(path="/", cache=BLOCK_TIME)
    async def get_transactions(
        self,
        limit: int = 100,
        skip: int = 0,
        sort: str = "desc",
        from_address: str = None,
        to_address: str = None,
        type: str = None,
        block_number: int = None,
        start_block_number: int = None,
        end_block_number: int = None,
        method: str = None,
    ) -> list[IcxTransaction]:
        """
        Returns a list of ICX transactions.
        """
        transactions = await Tracker.get_transactions(
            limit=limit,
            skip=skip,
            sort=sort,
            from_address=from_address,
            to_address=to_address,
            type=type,
            block_number=block_number,
            start_block_number=start_block_number,
            end_block_number=end_block_number,
            method=method,
        )
        return transactions
