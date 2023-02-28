from icon_rhizome_dev.balanced import Balanced
from icon_rhizome_dev.tokens import Tokens


class BalancedOracle(Balanced):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    async def get_price_in_usd(
        cls,
        token_symbol: str,
        block_number: int = 0,
        in_loop: bool = False,
    ) -> float | int:
        params = {"symbol": token_symbol}
        result = await cls.call(
            cls.CONTRACT_BALANCED_ORACLE,
            "getLastPriceInUSD",
            params,
            block_number=block_number,
        )
        if in_loop is True:
            return result
        else:
            return result
