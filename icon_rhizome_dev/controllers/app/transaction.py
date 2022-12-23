from starlite import Controller, get

from icon_rhizome_dev.constants import API_PREFIX


class AppTransactionController(Controller):
    """
    A controller for routes relating to ICON governance.
    """

    path = f"{API_PREFIX}/transactions"

    @get(path="/")
    async def get_validators(self):
        """
        Returns information about all ICON validators.
        """
        return
