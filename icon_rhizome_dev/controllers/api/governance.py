from starlite import Controller, get

from icon_rhizome_dev.constants import API_PREFIX


class ApiGovernanceController(Controller):
    """
    A controller for routes relating to ICON governance.
    """

    path = f"{API_PREFIX}/governance"

    @get(path="/validators/{address:str}/")
    async def get_validator(self, address: str):
        """
        Returns information about an ICON validator.

        Args:
            address: The ICX address of an ICON validator.
        """
        return

    @get(path="/validators/")
    async def get_validators(self):
        """
        Returns information about all ICON validators.
        """
        return
