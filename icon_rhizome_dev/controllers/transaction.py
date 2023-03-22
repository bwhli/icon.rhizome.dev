import asyncio
from datetime import datetime

from starlite import Controller, get, post

from icon_rhizome_dev.constants import API_PREFIX, BLOCK_TIME
from icon_rhizome_dev.icx import Icx
from icon_rhizome_dev.icx_utils import IcxUtils
from icon_rhizome_dev.models.icx import IcxTransaction
from icon_rhizome_dev.models.tracker import TrackerTransaction
from icon_rhizome_dev.tracker import Tracker


class TransactionController(Controller):
    """
    A controller for routes relating to ICX transactions.
    """

    path = f"/transactions"

    @get(path="/{tx_hash:str}/", cache=BLOCK_TIME)
    async def get_transaction(self, tx_hash: str) -> IcxTransaction:
        """
        Returns details about an ICX transaction.

        Args:
            tx_hash: An ICX transaction hash.
        """
        transaction = await Tracker.get_transaction(tx_hash)
        return transaction

    @post(path="/calculate-usd-value/")
    async def calculate_usd_value(self, data: dict[str, list[str]]) -> dict[str, float]:
        """
        Calculates USD value of ICX transactions.
        """
        results = []
        transaction_hashes = data["transaction_hashes"]

        async def _process(transaction_hash: str):
            transaction: TrackerTransaction = await Tracker.get_transaction(transaction_hash)  # fmt: skip
            icx_usd_price = await Icx.get_icx_usd_price(transaction.block_number)
            results.append(
                {
                    "tx_hash": transaction_hash,
                    "timestamp": datetime.utcfromtimestamp(
                        transaction.block_timestamp / 1_000_000
                    ),
                    "icx_amount": transaction.value_decimal,
                    "usd_value": transaction.value_decimal * icx_usd_price,
                }
            )

        await asyncio.gather(
            *[_process(transaction_hash) for transaction_hash in transaction_hashes]
        )

        return sorted(results, key=lambda x: x["timestamp"])

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
