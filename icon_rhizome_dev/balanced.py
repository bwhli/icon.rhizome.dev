from rich import print

from icon_rhizome_dev.icx_async import IcxAsync
from icon_rhizome_dev.models.balanced import BalancedLoan


class Balanced(IcxAsync):

    CONTRACT_BALANCED_LOANS = "cx66d4d90f5f113eba575bf793570135f9b10cece1"
    CONTRACT_BALANCED_PEG_STABILITY = "cxa09dbb60dcb62fffbd232b6eae132d730a2aafa6"

    def __init__(self) -> None:
        pass

    @classmethod
    async def get_loan_position(
        cls,
        address: str,
        block_number: int = 0,
    ) -> BalancedLoan:
        result = await cls.call(
            cls.CONTRACT_BALANCED_LOANS,
            "getAccountPositions",
            {"_owner": address},
            block_number=block_number,
        )
        return BalancedLoan(**result)

    @classmethod
    async def get_stability_fund_tokens(cls) -> list[str]:
        result = await cls.call(
            cls.CONTRACT_BALANCED_PEG_STABILITY,
            "getAcceptedTokens",
        )
        return result
