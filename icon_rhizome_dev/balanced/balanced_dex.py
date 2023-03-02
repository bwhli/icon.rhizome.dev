import asyncio
from datetime import datetime

from pydantic import BaseModel

from icon_rhizome_dev.balanced import Balanced
from icon_rhizome_dev.tokens import Tokens


class BalancedDividendClaim(BaseModel):
    contract: str
    symbol: str
    value: float
    value_in_usd: float | None = None
    transaction_hash: str
    block_number: int
    timestamp: datetime


class BalancedDex(Balanced):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    async def get_token_price_in_usd(
        cls,
        token_contract: str,
        block_number: int = 0,
    ) -> float:
        """
        Returns the USD price of an IRC-2 token at the specified block height.
        Currently supports BALN, bnUSD, and sICX.

        Args:
            token_contract: Contract address of an IRC-2 token.
            block_number: The block height to query.
        """
        if Tokens.get_symbol_by_contract(token_contract) == "BALN":
            print("Calculating BALN price in USD...")
            sicx_icx_price, sicx_baln_price, icx_usd_price = await asyncio.gather(
                *[
                    cls._get_price_by_name("sICX/ICX", block_number=block_number),
                    cls._get_price_by_name("BALN/sICX", block_number=block_number),
                    cls.get_icx_usd_price(block_number=block_number),
                ]
            )
            price = sicx_icx_price * sicx_baln_price * icx_usd_price
        elif Tokens.get_symbol_by_contract(token_contract) == "bnUSD":
            print("Calculating bnUSD price in USD...")
            sicx_icx_price, sicx_bnusd, icx_usd_price = await asyncio.gather(
                *[
                    cls._get_price_by_name("sICX/ICX", block_number=block_number),
                    cls._get_price_by_name("sICX/bnUSD", block_number=block_number),
                    cls.get_icx_usd_price(block_number=block_number),
                ]
            )
            price = (1 / sicx_bnusd) * sicx_icx_price * icx_usd_price
        elif Tokens.get_symbol_by_contract(token_contract) == "sICX":
            print("Calculating sICX price in USD...")
            sicx_icx_price, icx_usd_price = await asyncio.gather(
                *[
                    cls._get_price_by_name("sICX/ICX", block_number=block_number),
                    cls.get_icx_usd_price(block_number=block_number),
                ]
            )
            price = sicx_icx_price * icx_usd_price
        else:
            raise Exception(f"{token_contract} is not a supported contract.")

        return price

    @classmethod
    async def _get_price_by_name(
        cls,
        pool_name: str,
        block_number: int = 0,
    ):
        """
        An internal method for fetching a price quote for a Balanced pool.

        Args:
            pool_name: Name of a Balanced pool.
            block_number: The block height to query.
        """
        params = {"_name": pool_name}
        result = await cls.call(
            cls.CONTRACT_BALANCED_DEX,
            "getPriceByName",
            params,
            block_number=block_number,
        )
        price = result / 10**18
        return price
