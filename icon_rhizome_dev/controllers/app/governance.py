from starlite import Controller, get

from icon_rhizome_dev.constants import API_PREFIX


class AppGovernanceController(Controller):
    """
    A controller for routes relating to ICON governance.
    """

    path = f"{API_PREFIX}/governance"

    @get(path="/validators/")
    async def get_validators(self):
        """
        Returns information about all ICON validators.
        """
        return
