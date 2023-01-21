from icon_rhizome_dev.icx_async import IcxAsync


class Balanced(IcxAsync):

    CONTRACT_BALANCED_LOANS = "cx66d4d90f5f113eba575bf793570135f9b10cece1"

    def __init__(self) -> None:
        pass

    @classmethod
    async def get_loan_position(
        cls,
        address: str,
        block_number: int = 0,
    ):
        result = await cls.call(
            cls.CONTRACT_BALANCED_LOANS,
            "getAccountPositions",
            {"_owner": address},
            block_number=block_number,
        )
        return
