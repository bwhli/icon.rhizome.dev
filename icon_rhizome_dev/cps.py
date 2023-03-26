from icon_rhizome_dev.icx import Icx
from icon_rhizome_dev.models.cps import CpsProposal


class Cps(Icx):

    CPS_SCORE = "cx9f4ab72f854d3ccdc59aa6f2c3e2215dd62e879f"

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    async def get_proposal_details(
        cls,
        proposal_id: str,
        block_number: int = 0,
    ):
        result = await cls.call(
            cls.CPS_SCORE,
            "getProposalDetailsByHash",
            {"ipfsKey": proposal_id},
            block_number=block_number,
        )
        print(CpsProposal(**result))
        return CpsProposal(**result)
