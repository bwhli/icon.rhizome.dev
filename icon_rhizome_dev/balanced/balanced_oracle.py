from icon_rhizome_dev.balanced import BalancedBase
from icon_rhizome_dev.tokens import Tokens


class BalancedOracle(BalancedBase):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    async def get_price_in_usd(
        cls,
        token_symbol: str,
        in_loop: bool = False,
    ) -> float | int:
        params = {"symbol": token_symbol}
        result = await cls.call(
            cls.CONTRACT_BALANCED_ORACLE,
            "getLastPriceInUSD",
            params,
        )
        if in_loop is True:
            return result
        else:
            return result / 10 ** Tokens.get_decimals_by_contract()
