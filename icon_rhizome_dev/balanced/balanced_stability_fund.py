from icon_rhizome_dev.balanced import Balanced
from icon_rhizome_dev.tokens import Tokens


class BalancedStabilityFund(Balanced):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    async def get_stability_fund_tokens(cls) -> list[str]:
        result = await cls.call(
            cls.CONTRACT_BALANCED_PEG_STABILITY,
            "getAcceptedTokens",
        )
        return result
