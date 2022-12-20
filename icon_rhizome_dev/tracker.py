from icon_rhizome_dev.http import Http
from icon_rhizome_dev.models.transaction import Transaction


class Tracker:

    TRACKER_API_ENDPOINT = "https://tracker.icon.community/api/v1"

    def __init__(self) -> None:
        pass

    @classmethod
    async def get_transaction(cls, tx_hash: str) -> Transaction:
        response = await Http.get(f"{cls.TRACKER_API_ENDPOINT}/transaction/details/{tx_hash}")  # fmt: skip
        transaction = Transaction(**response)
        return transaction

    @classmethod
    async def get_transactions(cls) -> list[Transaction]:
        response = await Http.get(f"{cls.TRACKER_API_ENDPOINT}/transactions")
        transactions = [Transaction(**transaction) for transaction in response]
        return transactions
