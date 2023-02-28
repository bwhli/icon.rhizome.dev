from icon_rhizome_dev.balanced import Balanced
from icon_rhizome_dev.models.balanced import BalancedLoan


class BalancedLoans(Balanced):
    def __init__(self) -> None:
        super().__init__()

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
