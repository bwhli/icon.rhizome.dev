from icon_rhizome_dev.icx import Icx
from icon_rhizome_dev.models.tracker import TrackerTransaction
from icon_rhizome_dev.tracker import Tracker


class IcxUtils:
    def __init__(self) -> None:
        pass

    @classmethod
    async def calculate_transaction_usd_value(
        cls, transaction: TrackerTransaction
    ) -> float:
        icx_usd_price = await Icx.get_icx_usd_price(transaction.block_number)
        return transaction.value_decimal * icx_usd_price
