from starlite import Body, Controller, RequestEncodingType, Template, get, post

from icon_rhizome_dev.cps import Cps
from icon_rhizome_dev.utils import Utils


class CpsController(Controller):
    """
    A controller for routes relating to ICX transactions.
    """

    path = f"/cps"

    @get(path="/")
    async def get_cps(self) -> Template:
        return Template(
            name="cps/index.html",
            context={
                "title": "ICON Tools",
            },
        )

    @get(path="/proposal/{proposal_id:str}/")
    async def get_proposal(
        self,
        proposal_id: str,
        block_number: int = 0,
    ) -> Template:
        proposal_details = await Cps.get_proposal_details(
            proposal_id,
            block_number=block_number,
        )
        proposal_metadata = await Utils.get_ipfs_content(proposal_id)
        return Template(
            name="cps/proposal.html",
            context={
                "proposal_details": proposal_details,
                "proposal_description": proposal_metadata["description"],
            },
        )
